import logging
import socket
import asyncio
from collections import OrderedDict
from typing import Dict, List, Union, Type
from aioupnp.util import get_dict_val_case_insensitive, BASE_PORT_REGEX, BASE_ADDRESS_REGEX
from aioupnp.constants import SPEC_VERSION, SERVICE
from aioupnp.commands import SOAPCommands
from aioupnp.device import Device, Service
from aioupnp.protocols.ssdp import fuzzy_m_search, m_search
from aioupnp.protocols.scpd import scpd_get
from aioupnp.serialization.ssdp import SSDPDatagram
from aioupnp.util import flatten_keys
from aioupnp.fault import UPnPError

log = logging.getLogger(__name__)

return_type_lambas = {
    Union[None, str]: lambda x: x if x is not None and str(x).lower() not in ['none', 'nil'] else None
}


def get_action_list(element_dict: dict) -> List:  # [(<method>, [<input1>, ...], [<output1, ...]), ...]
    service_info = flatten_keys(element_dict, "{%s}" % SERVICE)
    if "actionList" in service_info:
        action_list = service_info["actionList"]
    else:
        return []
    if not len(action_list):  # it could be an empty string
        return []

    result: list = []
    if isinstance(action_list["action"], dict):
        arg_dicts = action_list["action"]['argumentList']['argument']
        if not isinstance(arg_dicts, list):  # when there is one arg
            arg_dicts = [arg_dicts]
        return [[
            action_list["action"]['name'],
            [i['name'] for i in arg_dicts if i['direction'] == 'in'],
            [i['name'] for i in arg_dicts if i['direction'] == 'out']
        ]]
    for action in action_list["action"]:
        if not action.get('argumentList'):
            result.append((action['name'], [], []))
        else:
            arg_dicts = action['argumentList']['argument']
            if not isinstance(arg_dicts, list):  # when there is one arg
                arg_dicts = [arg_dicts]
            result.append((
                action['name'],
                [i['name'] for i in arg_dicts if i['direction'] == 'in'],
                [i['name'] for i in arg_dicts if i['direction'] == 'out']
            ))
    return result


class Gateway:
    def __init__(self, ok_packet: SSDPDatagram, m_search_args: OrderedDict, lan_address: str,
                 gateway_address: str) -> None:
        self._ok_packet = ok_packet
        self._m_search_args = m_search_args
        self._lan_address = lan_address
        self.usn = (ok_packet.usn or '').encode()
        self.ext = (ok_packet.ext or '').encode()
        self.server = (ok_packet.server or '').encode()
        self.location = (ok_packet.location or '').encode()
        self.cache_control = (ok_packet.cache_control or '').encode()
        self.date = (ok_packet.date or '').encode()
        self.urn = (ok_packet.st or '').encode()

        self._xml_response = b""
        self._service_descriptors: Dict = {}
        self.base_address = BASE_ADDRESS_REGEX.findall(self.location)[0]
        self.port = int(BASE_PORT_REGEX.findall(self.location)[0])
        self.base_ip = self.base_address.lstrip(b"http://").split(b":")[0]
        assert self.base_ip == gateway_address.encode()
        self.path = self.location.split(b"%s:%i/" % (self.base_ip, self.port))[1]

        self.spec_version = None
        self.url_base = None

        self._device: Union[None, Device] = None
        self._devices: List = []
        self._services: List = []

        self._unsupported_actions: Dict = {}
        self._registered_commands: Dict = {}
        self.commands = SOAPCommands()

    def gateway_descriptor(self) -> dict:
        r = {
            'server': self.server.decode(),
            'urlBase': self.url_base,
            'location': self.location.decode(),
            "specVersion": self.spec_version,
            'usn': self.usn.decode(),
            'urn': self.urn.decode(),
        }
        return r

    @property
    def manufacturer_string(self) -> str:
        if not self.devices:
            return "UNKNOWN GATEWAY"
        device = list(self.devices.values())[0]
        return "%s %s" % (device.manufacturer, device.modelName)

    @property
    def services(self) -> Dict:
        if not self._device:
            return {}
        return {service.serviceType: service for service in self._services}

    @property
    def devices(self) -> Dict:
        if not self._device:
            return {}
        return {device.udn: device for device in self._devices}

    def get_service(self, service_type: str) -> Union[Type[Service], None]:
        for service in self._services:
            if service.serviceType.lower() == service_type.lower():
                return service
        return None

    @property
    def soap_requests(self) -> List:
        soap_call_infos = []
        for name in self._registered_commands.keys():
            if not hasattr(getattr(self.commands, name), "_requests"):
                continue
            soap_call_infos.extend([
                (name, request_args, raw_response, decoded_response, soap_error, ts)
                for (
                    request_args, raw_response, decoded_response, soap_error, ts
                ) in getattr(self.commands, name)._requests
            ])
        soap_call_infos.sort(key=lambda x: x[5])
        return soap_call_infos

    def debug_gateway(self) -> Dict:
        return {
            'manufacturer_string': self.manufacturer_string,
            'gateway_address': self.base_ip,
            'gateway_descriptor': self.gateway_descriptor(),
            'gateway_xml': self._xml_response,
            'services_xml': self._service_descriptors,
            'services': {service.SCPDURL: service.as_dict() for service in self._services},
            'm_search_args': [(k, v) for (k, v) in self._m_search_args.items()],
            'reply': self._ok_packet.as_dict(),
            'soap_port': self.port,
            'registered_soap_commands': self._registered_commands,
            'unsupported_soap_commands': self._unsupported_actions,
            'soap_requests': self.soap_requests
        }

    @classmethod
    async def _discover_gateway(cls, lan_address: str, gateway_address: str, timeout: int = 30,
                                igd_args: OrderedDict = None, loop=None, unicast: bool = False):
        ignored: set = set()
        required_commands = [
            'AddPortMapping',
            'DeletePortMapping',
            'GetExternalIPAddress'
        ]
        while True:
            if not igd_args:
                m_search_args, datagram = await fuzzy_m_search(
                    lan_address, gateway_address, timeout, loop,  ignored, unicast
                )
            else:
                m_search_args = OrderedDict(igd_args)
                datagram = await m_search(lan_address, gateway_address, igd_args, timeout, loop, ignored, unicast)
            try:
                gateway = cls(datagram, m_search_args, lan_address, gateway_address)
                log.debug('get gateway descriptor %s', datagram.location)
                await gateway.discover_commands(loop)
                requirements_met = all([required in gateway._registered_commands for required in required_commands])
                if not requirements_met:
                    not_met = [
                        required for required in required_commands if required not in gateway._registered_commands
                    ]
                    log.debug("found gateway %s at %s, but it does not implement required soap commands: %s",
                              gateway.manufacturer_string, gateway.location, not_met)
                    ignored.add(datagram.location)
                    continue
                else:
                    log.debug('found gateway device %s', datagram.location)
                    return gateway
            except (asyncio.TimeoutError, UPnPError) as err:
                log.debug("get %s failed (%s), looking for other devices", datagram.location, str(err))
                ignored.add(datagram.location)
                continue

    @classmethod
    async def discover_gateway(cls, lan_address: str, gateway_address: str, timeout: int = 30,
                               igd_args: OrderedDict = None, loop=None, unicast: bool = None):
        if unicast is not None:
            return await cls._discover_gateway(lan_address, gateway_address, timeout, igd_args, loop, unicast)

        done, pending = await asyncio.wait([
            cls._discover_gateway(
                lan_address, gateway_address, timeout, igd_args, loop, unicast=True
            ),
            cls._discover_gateway(
                lan_address, gateway_address, timeout, igd_args, loop, unicast=False
            )
        ], return_when=asyncio.tasks.FIRST_COMPLETED)

        for task in pending:
            task.cancel()
        for task in done:
            try:
                task.exception()
            except asyncio.CancelledError:
                pass

        return list(done)[0].result()

    async def discover_commands(self, loop=None):
        response, xml_bytes, get_err = await scpd_get(self.path.decode(), self.base_ip.decode(), self.port, loop=loop)
        self._xml_response = xml_bytes
        if get_err is not None:
            raise get_err
        self.spec_version = get_dict_val_case_insensitive(response, SPEC_VERSION)
        self.url_base = get_dict_val_case_insensitive(response, "urlbase")
        if not self.url_base:
            self.url_base = self.base_address.decode()
        if response:
            device_dict = get_dict_val_case_insensitive(response, "device")
            self._device = Device(
                self._devices, self._services, **device_dict
            )
        else:
            self._device = Device(self._devices, self._services)
        for service_type in self.services.keys():
            await self.register_commands(self.services[service_type], loop)

    async def register_commands(self, service: Service, loop=None):
        if not service.SCPDURL:
            raise UPnPError("no scpd url")

        log.debug("get descriptor for %s from %s", service.serviceType, service.SCPDURL)
        service_dict, xml_bytes, get_err = await scpd_get(service.SCPDURL, self.base_ip.decode(), self.port)
        self._service_descriptors[service.SCPDURL] = xml_bytes

        if get_err is not None:
            log.debug("failed to get descriptor for %s from %s", service.serviceType, service.SCPDURL)
            if xml_bytes:
                log.debug("response: %s", xml_bytes.decode())
            return
        if not service_dict:
            return

        action_list = get_action_list(service_dict)

        for name, inputs, outputs in action_list:
            try:
                self.commands.register(self.base_ip, self.port, name, service.controlURL, service.serviceType.encode(),
                                       inputs, outputs, loop)
                self._registered_commands[name] = service.serviceType
                log.debug("registered %s::%s", service.serviceType, name)
            except AttributeError:
                s = self._unsupported_actions.get(service.serviceType, [])
                s.append(name)
                self._unsupported_actions[service.serviceType] = s
                log.debug("available command for %s does not have a wrapper implemented: %s %s %s",
                          service.serviceType, name, inputs, outputs)
            log.debug("registered service %s", service.serviceType)
