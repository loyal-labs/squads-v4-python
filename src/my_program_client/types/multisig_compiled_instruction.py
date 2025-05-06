from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class MultisigCompiledInstructionJSON(typing.TypedDict):
    program_id_index: int
    account_indexes: list[int]
    data: list[int]


@dataclass
class MultisigCompiledInstruction:
    layout: typing.ClassVar = borsh.CStruct(
        "program_id_index" / borsh.U8,
        "account_indexes" / borsh.Bytes,
        "data" / borsh.Bytes,
    )
    program_id_index: int
    account_indexes: bytes
    data: bytes

    @classmethod
    def from_decoded(cls, obj: Container) -> "MultisigCompiledInstruction":
        return cls(
            program_id_index=obj.program_id_index,
            account_indexes=obj.account_indexes,
            data=obj.data,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "program_id_index": self.program_id_index,
            "account_indexes": self.account_indexes,
            "data": self.data,
        }

    def to_json(self) -> MultisigCompiledInstructionJSON:
        return {
            "program_id_index": self.program_id_index,
            "account_indexes": list(self.account_indexes),
            "data": list(self.data),
        }

    @classmethod
    def from_json(
        cls, obj: MultisigCompiledInstructionJSON
    ) -> "MultisigCompiledInstruction":
        return cls(
            program_id_index=obj["program_id_index"],
            account_indexes=bytes(obj["account_indexes"]),
            data=bytes(obj["data"]),
        )
