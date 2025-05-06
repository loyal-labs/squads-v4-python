from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh


class MultisigMessageAddressTableLookupJSON(typing.TypedDict):
    account_key: str
    writable_indexes: list[int]
    readonly_indexes: list[int]


@dataclass
class MultisigMessageAddressTableLookup:
    layout: typing.ClassVar = borsh.CStruct(
        "account_key" / BorshPubkey,
        "writable_indexes" / borsh.Bytes,
        "readonly_indexes" / borsh.Bytes,
    )
    account_key: Pubkey
    writable_indexes: bytes
    readonly_indexes: bytes

    @classmethod
    def from_decoded(cls, obj: Container) -> "MultisigMessageAddressTableLookup":
        return cls(
            account_key=obj.account_key,
            writable_indexes=obj.writable_indexes,
            readonly_indexes=obj.readonly_indexes,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "account_key": self.account_key,
            "writable_indexes": self.writable_indexes,
            "readonly_indexes": self.readonly_indexes,
        }

    def to_json(self) -> MultisigMessageAddressTableLookupJSON:
        return {
            "account_key": str(self.account_key),
            "writable_indexes": list(self.writable_indexes),
            "readonly_indexes": list(self.readonly_indexes),
        }

    @classmethod
    def from_json(
        cls, obj: MultisigMessageAddressTableLookupJSON
    ) -> "MultisigMessageAddressTableLookup":
        return cls(
            account_key=Pubkey.from_string(obj["account_key"]),
            writable_indexes=bytes(obj["writable_indexes"]),
            readonly_indexes=bytes(obj["readonly_indexes"]),
        )
