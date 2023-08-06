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

import hashlib
from enum import Enum
from typing import NewType, Tuple

import construct as c
import ecdsa
import pyblake2

from . import cosi, messages, tools

V1_SIGNATURE_SLOTS = 3
V1_BOOTLOADER_KEYS = {
    1: "04c2e313b6443f1be1305cf711a788fc0dedf82c59ca2fdc5254fe6f4330abe659cf174f61736b4042842693d6bf6173f5ce5c127adf0b92ade5b82116ec7f21a9",
    2: "047dfc172a1f74207ad925e53ab37b63ad22c58ae9e31ef8634971ad59ffad7ecb5b76b7eca61ce1b8e537588f857dcf7cf7e7f7fb876ca8582b893be5c6b7cb90",
    3: "0405501e87cc710eff44083d5f80338d82280235bd5def4310a16d05601663080a859fdb6ecb5297d3930d2c3842ff19a63e04e2ec8d2cdd63d1c5a0af38aa3008",
    4: "04a2e4af10c52c628ffb57a6dbeabb5f4dead1575772719a194b6dc9c51be53b09544ca3f16dfc4e0c86103287a23f80ee54227811252b50688bd55ec66f4de474",
    5: "04f8b27de9917ec25b0733982194cbe1f41b0ea257f7defef1c7203c5fb9483ff0b22a82ec72d214efe0ec6cfd15358bfd6629b1db39b6af071c73fa0f0bb58102",
}

V2_BOOTLOADER_KEYS = [
    bytes.fromhex("c2c87a49c5a3460977fbb2ec9dfe60f06bd694db8244bd4981fe3b7a26307f3f"),
    bytes.fromhex("80d036b08739b846f4cb77593078deb25dc9487aedcf52e30b4fb7cd7024178a"),
    bytes.fromhex("b8307a71f552c60a4cbb317ff48b82cdbf6b6bb5f04c920fec7badf017883751"),
]
V2_BOOTLOADER_M = 2
V2_BOOTLOADER_N = 3

V2_CHUNK_SIZE = 1024 * 128


def _transform_vendor_trust(data: bytes) -> bytes:
    """Byte-swap and bit-invert the VendorTrust field.

    Vendor trust is interpreted as a bitmask in a 16-bit little-endian integer,
    with the added twist that 0 means set and 1 means unset.
    We feed it to a `BitStruct` that expects a big-endian sequence where bits have
    the traditional meaning. We must therefore do a bitwise negation of each byte,
    and return them in reverse order. This is the same transformation both ways,
    fortunately, so we don't need two separate functions.
    """
    return bytes(~b & 0xFF for b in data)[::-1]


# fmt: off
Toif = c.Struct(
    "magic" / c.Const(b"TOI"),
    "format" / c.Enum(c.Byte, full_color=b"f", grayscale=b"g"),
    "width" / c.Int16ul,
    "height" / c.Int16ul,
    "data" / c.Prefixed(c.Int32ul, c.GreedyBytes),
)


VendorTrust = c.Transformed(c.BitStruct(
    "reserved" / c.Default(c.BitsInteger(9), 0),
    "show_vendor_string" / c.Flag,
    "require_user_click" / c.Flag,
    "red_background" / c.Flag,
    "delay" / c.BitsInteger(4),
), _transform_vendor_trust, 2, _transform_vendor_trust, 2)


VendorHeader = c.Struct(
    "_start_offset" / c.Tell,
    "magic" / c.Const(b"TRZV"),
    "_header_len" / c.Padding(4),
    "expiry" / c.Int32ul,
    "version" / c.Struct(
        "major" / c.Int8ul,
        "minor" / c.Int8ul,
    ),
    "vendor_sigs_required" / c.Int8ul,
    "vendor_sigs_n" / c.Rebuild(c.Int8ul, c.len_(c.this.pubkeys)),
    "vendor_trust" / VendorTrust,
    "reserved" / c.Padding(14),
    "pubkeys" / c.Bytes(32)[c.this.vendor_sigs_n],
    "vendor_string" / c.Aligned(4, c.PascalString(c.Int8ul, "utf-8")),
    "vendor_image" / Toif,
    "_data_end_offset" / c.Tell,

    c.Padding(-(c.this._data_end_offset + 65) % 512),
    "sigmask" / c.Byte,
    "signature" / c.Bytes(64),

    "_end_offset" / c.Tell,
    "header_len" / c.Pointer(
        c.this._start_offset + 4,
        c.Rebuild(c.Int32ul, c.this._end_offset - c.this._start_offset)
    ),
)


VersionLong = c.Struct(
    "major" / c.Int8ul,
    "minor" / c.Int8ul,
    "patch" / c.Int8ul,
    "build" / c.Int8ul,
)


FirmwareHeader = c.Struct(
    "_start_offset" / c.Tell,
    "magic" / c.Const(b"TRZF"),
    "_header_len" / c.Padding(4),
    "expiry" / c.Int32ul,
    "code_length" / c.Rebuild(
        c.Int32ul,
        lambda this:
            len(this._.code) if "code" in this._
            else (this.code_length or 0)
    ),
    "version" / VersionLong,
    "fix_version" / VersionLong,
    "reserved" / c.Padding(8),
    "hashes" / c.Bytes(32)[16],

    "reserved" / c.Padding(415),
    "sigmask" / c.Byte,
    "signature" / c.Bytes(64),

    "_end_offset" / c.Tell,
    "header_len" / c.Pointer(
        c.this._start_offset + 4,
        c.Rebuild(c.Int32ul, c.this._end_offset - c.this._start_offset)
    ),
)


Firmware = c.Struct(
    "vendor_header" / VendorHeader,
    "firmware_header" / FirmwareHeader,
    "_code_offset" / c.Tell,
    "code" / c.Bytes(c.this.firmware_header.code_length),
    c.Terminated,
)


FirmwareV1 = c.Struct(
    "magic" / c.Const(b"TRZR"),
    "code_length" / c.Rebuild(c.Int32ul, c.len_(c.this.code)),
    "key_indexes" / c.Int8ul[V1_SIGNATURE_SLOTS],  # pylint: disable=E1136
    "flags" / c.BitStruct(
        c.Padding(7),
        "restore_storage" / c.Flag,
    ),
    "reserved" / c.Padding(52),
    "signatures" / c.Bytes(64)[V1_SIGNATURE_SLOTS],
    "code" / c.Bytes(c.this.code_length),
    c.Terminated,
)

# fmt: on


class FirmwareFormat(Enum):
    SafeWISE_ONE = 1
    SafeWISE_T = 2


FirmwareType = NewType("FirmwareType", c.Container)
ParsedFirmware = Tuple[FirmwareFormat, FirmwareType]


def parse(data: bytes) -> ParsedFirmware:
    if data[:4] == b"TRZR":
        version = FirmwareFormat.SafeWISE_ONE
        cls = FirmwareV1
    elif data[:4] == b"TRZV":
        version = FirmwareFormat.SafeWISE_T
        cls = Firmware
    else:
        raise ValueError("Unrecognized firmware image type")

    try:
        fw = cls.parse(data)
    except Exception as e:
        raise ValueError("Invalid firmware image") from e
    return version, FirmwareType(fw)


def digest_v1(fw: FirmwareType) -> bytes:
    return hashlib.sha256(fw.code).digest()


def check_sig_v1(fw: FirmwareType, idx: int) -> bool:
    key_idx = fw.key_indexes[idx]
    signature = fw.signatures[idx]

    if key_idx == 0:
        # no signature = invalid signature
        return False

    if key_idx not in V1_BOOTLOADER_KEYS:
        # unknown pubkey
        return False

    pubkey = bytes.fromhex(V1_BOOTLOADER_KEYS[key_idx])[1:]
    verify = ecdsa.VerifyingKey.from_string(
        pubkey, curve=ecdsa.curves.SECP256k1, hashfunc=hashlib.sha256
    )
    try:
        verify.verify(signature, fw.code)
        return True
    except ecdsa.BadSignatureError:
        return False


def _header_digest(header: c.Container, header_type: c.Construct) -> bytes:
    stripped_header = header.copy()
    stripped_header.sigmask = 0
    stripped_header.signature = b"\0" * 64
    header_bytes = header_type.build(stripped_header)
    return pyblake2.blake2s(header_bytes).digest()


def digest(fw: FirmwareType) -> bytes:
    return _header_digest(fw.firmware_header, FirmwareHeader)


def validate(fw: FirmwareType, skip_vendor_header=False) -> bool:
    vendor_fingerprint = _header_digest(fw.vendor_header, VendorHeader)
    fingerprint = digest(fw)

    if not skip_vendor_header:
        try:
            # if you want to validate a custom vendor header, you can modify
            # the global variables to match your keys and m-of-n scheme
            cosi.verify_m_of_n(
                fw.vendor_header.signature,
                vendor_fingerprint,
                V2_BOOTLOADER_M,
                V2_BOOTLOADER_N,
                fw.vendor_header.sigmask,
                V2_BOOTLOADER_KEYS,
            )
        except Exception:
            raise ValueError("Invalid vendor header signature.")

        # XXX expiry is not used now
        # now = time.gmtime()
        # if time.gmtime(fw.vendor_header.expiry) < now:
        #     raise ValueError("Vendor header expired.")

    try:
        cosi.verify_m_of_n(
            fw.firmware_header.signature,
            fingerprint,
            fw.vendor_header.vendor_sigs_required,
            fw.vendor_header.vendor_sigs_n,
            fw.firmware_header.sigmask,
            fw.vendor_header.pubkeys,
        )
    except Exception:
        raise ValueError("Invalid firmware signature.")

    # XXX expiry is not used now
    # if time.gmtime(fw.firmware_header.expiry) < now:
    #     raise ValueError("Firmware header expired.")

    for i, expected_hash in enumerate(fw.firmware_header.hashes):
        if i == 0:
            # Because first chunk is sent along with headers, there is less code in it.
            chunk = fw.code[: V2_CHUNK_SIZE - fw._code_offset]
        else:
            # Subsequent chunks are shifted by the "missing header" size.
            ptr = i * V2_CHUNK_SIZE - fw._code_offset
            chunk = fw.code[ptr : ptr + V2_CHUNK_SIZE]

        if not chunk and expected_hash == b"\0" * 32:
            continue
        chunk_hash = pyblake2.blake2s(chunk).digest()
        if chunk_hash != expected_hash:
            raise ValueError("Invalid firmware data.")

    return True


# ====== Client functions ====== #


@tools.session
def update(client, data):
    if client.features.bootloader_mode is False:
        raise RuntimeError("Device must be in bootloader mode")

    resp = client.call(messages.FirmwareErase(length=len(data)))

    # SafeWISEv1 method
    if isinstance(resp, messages.Success):
        resp = client.call(messages.FirmwareUpload(payload=data))
        if isinstance(resp, messages.Success):
            return
        else:
            raise RuntimeError("Unexpected result %s" % resp)

    # SafeWISEv2 method
    while isinstance(resp, messages.FirmwareRequest):
        payload = data[resp.offset : resp.offset + resp.length]
        digest = pyblake2.blake2s(payload).digest()
        resp = client.call(messages.FirmwareUpload(payload=payload, hash=digest))

    if isinstance(resp, messages.Success):
        return
    else:
        raise RuntimeError("Unexpected message %s" % resp)
