from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class TransactionBufferCreateArgsJSON(typing.TypedDict):
    buffer_index: int
    vault_index: int
    final_buffer_hash: list[int]
    final_buffer_size: int
    buffer: list[int]


@dataclass
class TransactionBufferCreateArgs:
    layout: typing.ClassVar = borsh.CStruct(
        "buffer_index" / borsh.U8,
        "vault_index" / borsh.U8,
        "final_buffer_hash" / borsh.U8[32],
        "final_buffer_size" / borsh.U16,
        "buffer" / borsh.Bytes,
    )
    buffer_index: int
    vault_index: int
    final_buffer_hash: list[int]
    final_buffer_size: int
    buffer: bytes

    @classmethod
    def from_decoded(cls, obj: Container) -> "TransactionBufferCreateArgs":
        return cls(
            buffer_index=obj.buffer_index,
            vault_index=obj.vault_index,
            final_buffer_hash=obj.final_buffer_hash,
            final_buffer_size=obj.final_buffer_size,
            buffer=obj.buffer,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "buffer_index": self.buffer_index,
            "vault_index": self.vault_index,
            "final_buffer_hash": self.final_buffer_hash,
            "final_buffer_size": self.final_buffer_size,
            "buffer": self.buffer,
        }

    def to_json(self) -> TransactionBufferCreateArgsJSON:
        return {
            "buffer_index": self.buffer_index,
            "vault_index": self.vault_index,
            "final_buffer_hash": self.final_buffer_hash,
            "final_buffer_size": self.final_buffer_size,
            "buffer": list(self.buffer),
        }

    @classmethod
    def from_json(
        cls, obj: TransactionBufferCreateArgsJSON
    ) -> "TransactionBufferCreateArgs":
        return cls(
            buffer_index=obj["buffer_index"],
            vault_index=obj["vault_index"],
            final_buffer_hash=obj["final_buffer_hash"],
            final_buffer_size=obj["final_buffer_size"],
            buffer=bytes(obj["buffer"]),
        )
