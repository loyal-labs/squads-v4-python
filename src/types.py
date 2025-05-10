from abc import ABC
from dataclasses import dataclass
from enum import IntFlag
from typing import Any

from anchorpy.borsh_extension import BorshPubkey  # type: ignore
from borsh_construct import U8, U16, CStruct  # type: ignore
from construct import Array, Construct, PrefixedArray
from solders.pubkey import Pubkey

from src.generated.types.multisig_compiled_instruction import (
    MultisigCompiledInstructionJSON,
)
from src.generated.types.multisig_message_address_table_lookup import (
    MultisigMessageAddressTableLookupJSON,
)
from src.generated.types.vault_transaction_message import VaultTransactionMessageJSON


def U8Vec(subcon: Construct) -> Array:  # type: ignore
    return PrefixedArray(U8, subcon)  # type: ignore


def U16Vec(subcon: Construct) -> Array:  # type: ignore
    return PrefixedArray(U16, subcon)  # type: ignore


@dataclass
class CompiledMsInstructionConstruct:
    program_id_index: int
    account_indexes: list[int]
    data: list[int]

    layout = CStruct(
        "program_id_index" / U8,
        "account_indexex" / U8Vec(U8),  # type: ignore
        "data" / U16Vec(U8),  # type: ignore
    )

    @classmethod
    def from_json(
        cls, obj: MultisigCompiledInstructionJSON
    ) -> "CompiledMsInstructionConstruct":
        return cls(
            program_id_index=obj["program_id_index"],
            account_indexes=obj["account_indexes"],
            data=obj["data"],
        )

    def to_encodable(self) -> dict[str, Any]:
        return {
            "program_id_index": self.program_id_index,
            "account_indexes": self.account_indexes,
            "data": self.data,
        }


@dataclass
class MessageAddressTableConstruct:
    account_key: Pubkey
    writable_indexes: list[int]
    readonly_indexes: list[int]

    layout = CStruct(
        "account_key" / BorshPubkey,  # type: ignore
        "writable_indexes" / U8Vec(U8),  # type: ignore
        "readonly_indexes" / U8Vec(U8),  # type: ignore
    )

    @classmethod
    def from_json(
        cls, obj: MultisigMessageAddressTableLookupJSON
    ) -> "MessageAddressTableConstruct":
        return cls(
            account_key=Pubkey.from_string(obj["account_key"]),
            writable_indexes=obj["writable_indexes"],
            readonly_indexes=obj["readonly_indexes"],
        )

    def to_encodable(self) -> dict[str, Any]:
        return {
            "account_key": str(self.account_key),
            "writable_indexes": self.writable_indexes,
            "readonly_indexes": self.readonly_indexes,
        }


@dataclass
class TransactionMessageConstruct:
    num_signers: int
    num_writable_signers: int
    num_writable_non_signers: int
    account_keys: list[Pubkey]
    instructions: list[CompiledMsInstructionConstruct]
    address_table_lookups: list[MessageAddressTableConstruct]

    layout = CStruct(
        "num_signers" / U8,
        "num_writable_signers" / U8,
        "num_writable_non_signers" / U8,
        "account_keys" / U8Vec(BorshPubkey),  # type: ignore
        "instructions" / U8Vec(CompiledMsInstructionConstruct),  # type: ignore
        "address_table_lookups" / U8Vec(MessageAddressTableConstruct),  # type: ignore
    )

    @classmethod
    def from_json(
        cls, obj: VaultTransactionMessageJSON
    ) -> "TransactionMessageConstruct":
        return cls(
            num_signers=obj["num_signers"],
            num_writable_signers=obj["num_writable_signers"],
            num_writable_non_signers=obj["num_writable_non_signers"],
            account_keys=[Pubkey.from_string(key) for key in obj["account_keys"]],
            instructions=[
                CompiledMsInstructionConstruct.from_json(instruction)
                for instruction in obj["instructions"]
            ],
            address_table_lookups=[
                MessageAddressTableConstruct.from_json(lookup)
                for lookup in obj["address_table_lookups"]
            ],
        )

    def to_encodable(self) -> dict[str, Any]:
        return {
            "num_signers": self.num_signers,
            "num_writable_signers": self.num_writable_signers,
            "num_writable_non_signers": self.num_writable_non_signers,
            "account_keys": [str(key) for key in self.account_keys],
            "instructions": [
                instruction.to_encodable() for instruction in self.instructions
            ],
            "address_table_lookups": [
                lookup.to_encodable() for lookup in self.address_table_lookups
            ],
        }


class Permission(IntFlag):
    initiate = 0b0000_0001
    vote = 0b0000_0010
    execute = 0b0000_0100


class AbstractPermissions(ABC):
    mask: int


class Permissions(AbstractPermissions):
    """Manages bitmask of permissions."""

    mask: int

    def __init__(self, mask: int):
        self.mask = mask

    @staticmethod
    def from_permissions(permissions: list[Permission]) -> "Permissions":
        """Creates a Permissions object from a list of Permission enum members."""
        mask = 0
        for p_flag in permissions:
            mask |= p_flag.value

        return Permissions(mask)

    @staticmethod
    def all() -> "Permissions":
        """Creates a Permissions object with all defined permissions."""
        mask = 0
        for p_flag in Permission:  # Iterates over all members of the IntFlag
            mask |= p_flag.value

        return Permissions(mask)

    @staticmethod
    def has(permissions_obj: AbstractPermissions, permission_flag: Permission) -> bool:
        """
        Checks if the given Permissions object (or any object with a mask)
        has a specific permission.
        """
        return (permissions_obj.mask & permission_flag.value) == permission_flag.value
