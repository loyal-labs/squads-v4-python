from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class BatchAddTransactionArgsJSON(typing.TypedDict):
    ephemeral_signers: int
    transaction_message: list[int]


@dataclass
class BatchAddTransactionArgs:
    layout: typing.ClassVar = borsh.CStruct(
        "ephemeral_signers" / borsh.U8, "transaction_message" / borsh.Bytes
    )
    ephemeral_signers: int
    transaction_message: bytes

    @classmethod
    def from_decoded(cls, obj: Container) -> "BatchAddTransactionArgs":
        return cls(
            ephemeral_signers=obj.ephemeral_signers,
            transaction_message=obj.transaction_message,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "ephemeral_signers": self.ephemeral_signers,
            "transaction_message": self.transaction_message,
        }

    def to_json(self) -> BatchAddTransactionArgsJSON:
        return {
            "ephemeral_signers": self.ephemeral_signers,
            "transaction_message": list(self.transaction_message),
        }

    @classmethod
    def from_json(cls, obj: BatchAddTransactionArgsJSON) -> "BatchAddTransactionArgs":
        return cls(
            ephemeral_signers=obj["ephemeral_signers"],
            transaction_message=bytes(obj["transaction_message"]),
        )
