from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class VaultTransactionCreateArgsJSON(typing.TypedDict):
    vault_index: int
    ephemeral_signers: int
    transaction_message: list[int]
    memo: typing.Optional[str]


@dataclass
class VaultTransactionCreateArgs:
    layout: typing.ClassVar = borsh.CStruct(
        "vault_index" / borsh.U8,
        "ephemeral_signers" / borsh.U8,
        "transaction_message" / borsh.Bytes,
        "memo" / borsh.Option(borsh.String),
    )
    vault_index: int
    ephemeral_signers: int
    transaction_message: bytes
    memo: typing.Optional[str]

    @classmethod
    def from_decoded(cls, obj: Container) -> "VaultTransactionCreateArgs":
        return cls(
            vault_index=obj.vault_index,
            ephemeral_signers=obj.ephemeral_signers,
            transaction_message=obj.transaction_message,
            memo=obj.memo,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "vault_index": self.vault_index,
            "ephemeral_signers": self.ephemeral_signers,
            "transaction_message": self.transaction_message,
            "memo": self.memo,
        }

    def to_json(self) -> VaultTransactionCreateArgsJSON:
        return {
            "vault_index": self.vault_index,
            "ephemeral_signers": self.ephemeral_signers,
            "transaction_message": list(self.transaction_message),
            "memo": self.memo,
        }

    @classmethod
    def from_json(
        cls, obj: VaultTransactionCreateArgsJSON
    ) -> "VaultTransactionCreateArgs":
        return cls(
            vault_index=obj["vault_index"],
            ephemeral_signers=obj["ephemeral_signers"],
            transaction_message=bytes(obj["transaction_message"]),
            memo=obj["memo"],
        )
