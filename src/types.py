from abc import ABC
from dataclasses import dataclass
from enum import IntFlag

from anchorpy.borsh_extension import BorshPubkey  # type: ignore
from borsh_construct import U8, U16, CStruct
from construct import Struct
from solders.pubkey import Pubkey

from src.utils.utils import create_small_array  # type: ignore


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


@dataclass
class CompiledInstructionMultisig:
    program_id_index: int
    account_indexes: list[int]
    data: list[int]

    @classmethod
    def construct(cls):
        return CStruct(
            "program_id_index" / U8,
            "account_indexes" / create_small_array(U8, U8),  # type: ignore
            "data" / create_small_array(U16, U8),  # type: ignore
        )


@dataclass
class MessageAddressTableLookup:
    account_key: Pubkey
    writable_indexes: list[int]
    readonly_indexes: list[int]

    @classmethod
    def construct(  # type: ignore
        cls,
    ) -> Struct:  # type: ignore
        return CStruct(
            "account_key" / BorshPubkey,  # type: ignore
            "writable_indexes" / create_small_array(U8, U8),  # type: ignore
            "readonly_indexes" / create_small_array(U8, U8),  # type: ignore
        )


@dataclass
class TransactionMessage:
    num_signers: int
    num_writable_signers: int
    num_writable_non_signers: int
    account_keys: list[Pubkey]
    instructions: list[CompiledInstructionMultisig]
    address_table_lookups: list[MessageAddressTableLookup]

    @classmethod
    def construct(  # type: ignore
        cls,
    ) -> Struct:  # type: ignore
        return CStruct(
            "num_signers" / U8,
            "num_writable_signers" / U8,
            "num_writable_non_signers" / U8,
            "account_keys" / create_small_array(U8, BorshPubkey),  # type: ignore
            "instructions" / create_small_array(U8, CompiledInstructionMultisig),  # type: ignore
            "address_table_lookups" / create_small_array(U8, MessageAddressTableLookup),  # type: ignore
        )
