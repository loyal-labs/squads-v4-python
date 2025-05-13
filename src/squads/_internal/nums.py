import struct
from typing import Any


def to_utf_bytes(s: str) -> bytes:
    return s.encode("utf-8")


def to_u8_bytes(num: int) -> bytes:
    return struct.pack("<B", num)


def to_u32_bytes(num: int) -> bytes:
    return struct.pack("<I", num)


def to_u64_bytes(num: int) -> bytes:
    return struct.pack("<Q", num)


def to_big_int(number: Any) -> int:
    return int(str(number))
