from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class TransactionBufferExtendArgsJSON(typing.TypedDict):
    buffer: list[int]


@dataclass
class TransactionBufferExtendArgs:
    layout: typing.ClassVar = borsh.CStruct("buffer" / borsh.Bytes)
    buffer: bytes

    @classmethod
    def from_decoded(cls, obj: Container) -> "TransactionBufferExtendArgs":
        return cls(buffer=obj.buffer)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"buffer": self.buffer}

    def to_json(self) -> TransactionBufferExtendArgsJSON:
        return {"buffer": list(self.buffer)}

    @classmethod
    def from_json(
        cls, obj: TransactionBufferExtendArgsJSON
    ) -> "TransactionBufferExtendArgs":
        return cls(buffer=bytes(obj["buffer"]))
