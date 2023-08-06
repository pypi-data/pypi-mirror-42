#
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 3
# as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the License along with this library.
# If not, see <https://www.gnu.org/licenses/lgpl-3.0.html>.

import logging
from typing import Iterable, List, Set, Type

from ..exceptions import SafeWISEException
from ..protobuf import MessageType

if False:
    # mark Set and List as used, otherwise they only exist in comments
    List, Set

LOG = logging.getLogger(__name__)

# USB vendor/product IDs for SafeWISEs
DEV_SafeWISE1 = (0x1209, 0xABBA)
DEV_SafeWISE2 = (0x1209, 0xABB9)
DEV_SafeWISE2_BL = (0x1209, 0xABB8)

SafeWISES = {DEV_SafeWISE1, DEV_SafeWISE2, DEV_SafeWISE2_BL}

UDEV_RULES_STR = """
Do you have udev rules installed?
https://wallet.safewise.io/data/50-safewise.rules
""".strip()


class TransportException(SafeWISEException):
    pass


class Transport:
    """Raw connection to a SafeWISE device.

    Transport subclass represents a kind of communication link: SafeWISE Bridge, WebUSB
    or USB-HID connection, or UDP socket of listening emulator(s).
    It can also enumerate devices available over this communication link, and return
    them as instances.

    Transport instance is a thing that:
    - can be identified and requested by a string URI-like path
    - can open and close sessions, which enclose related operations
    - can read and write protobuf messages

    You need to implement a new Transport subclass if you invent a new way to connect
    a SafeWISE device to a computer.
    """

    PATH_PREFIX = None  # type: str
    ENABLED = False

    def __str__(self) -> str:
        return self.get_path()

    def get_path(self) -> str:
        raise NotImplementedError

    def begin_session(self) -> None:
        raise NotImplementedError

    def end_session(self) -> None:
        raise NotImplementedError

    def read(self) -> MessageType:
        raise NotImplementedError

    def write(self, message: MessageType) -> None:
        raise NotImplementedError

    @classmethod
    def enumerate(cls) -> Iterable["Transport"]:
        raise NotImplementedError

    @classmethod
    def find_by_path(cls, path: str, prefix_search: bool = False) -> "Transport":
        for device in cls.enumerate():
            if (
                path is None
                or device.get_path() == path
                or (prefix_search and device.get_path().startswith(path))
            ):
                return device

        raise TransportException(
            "{} device not found: {}".format(cls.PATH_PREFIX, path)
        )


def all_transports() -> Iterable[Type[Transport]]:
    from .bridge import BridgeTransport
    from .hid import HidTransport
    from .udp import UdpTransport
    from .webusb import WebUsbTransport

    return set(
        cls
        for cls in (BridgeTransport, HidTransport, UdpTransport, WebUsbTransport)
        if cls.ENABLED
    )


def enumerate_devices() -> Iterable[Transport]:
    devices = []  # type: List[Transport]
    for transport in all_transports():
        name = transport.__name__
        try:
            found = list(transport.enumerate())
            LOG.info("Enumerating {}: found {} devices".format(name, len(found)))
            devices.extend(found)
        except NotImplementedError:
            LOG.error("{} does not implement device enumeration".format(name))
        except Exception as e:
            excname = e.__class__.__name__
            LOG.error("Failed to enumerate {}. {}: {}".format(name, excname, e))
    return devices


def get_transport(path: str = None, prefix_search: bool = False) -> Transport:
    if path is None:
        try:
            return next(iter(enumerate_devices()))
        except IndexError:
            raise Exception("No SafeWISE device found") from None

    # Find whether B is prefix of A (transport name is part of the path)
    # or A is prefix of B (path is a prefix, or a name, of transport).
    # This naively expects that no two transports have a common prefix.
    def match_prefix(a: str, b: str) -> bool:
        return a.startswith(b) or b.startswith(a)

    LOG.info(
        "looking for device by {}: {}".format(
            "prefix" if prefix_search else "full path", path
        )
    )
    transports = [t for t in all_transports() if match_prefix(path, t.PATH_PREFIX)]
    if transports:
        return transports[0].find_by_path(path, prefix_search=prefix_search)

    raise Exception("Could not find device by path: {}".format(path))
