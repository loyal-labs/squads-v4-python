from __future__ import annotations
from . import (
    multisig_compiled_instruction,
    multisig_message_address_table_lookup,
)
import typing
from dataclasses import dataclass
from construct import Container, Construct
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh


class VaultTransactionMessageJSON(typing.TypedDict):
    num_signers: int
    num_writable_signers: int
    num_writable_non_signers: int
    account_keys: list[str]
    instructions: list[multisig_compiled_instruction.MultisigCompiledInstructionJSON]
    address_table_lookups: list[
        multisig_message_address_table_lookup.MultisigMessageAddressTableLookupJSON
    ]


@dataclass
class VaultTransactionMessage:
    layout: typing.ClassVar = borsh.CStruct(
        "num_signers" / borsh.U8,
        "num_writable_signers" / borsh.U8,
        "num_writable_non_signers" / borsh.U8,
        "account_keys" / borsh.Vec(typing.cast(Construct, BorshPubkey)),
        "instructions"
        / borsh.Vec(
            typing.cast(
                Construct,
                multisig_compiled_instruction.MultisigCompiledInstruction.layout,
            )
        ),
        "address_table_lookups"
        / borsh.Vec(
            typing.cast(
                Construct,
                multisig_message_address_table_lookup.MultisigMessageAddressTableLookup.layout,
            )
        ),
    )
    num_signers: int
    num_writable_signers: int
    num_writable_non_signers: int
    account_keys: list[Pubkey]
    instructions: list[multisig_compiled_instruction.MultisigCompiledInstruction]
    address_table_lookups: list[
        multisig_message_address_table_lookup.MultisigMessageAddressTableLookup
    ]

    @classmethod
    def from_decoded(cls, obj: Container) -> "VaultTransactionMessage":
        return cls(
            num_signers=obj.num_signers,
            num_writable_signers=obj.num_writable_signers,
            num_writable_non_signers=obj.num_writable_non_signers,
            account_keys=obj.account_keys,
            instructions=list(
                map(
                    lambda item: multisig_compiled_instruction.MultisigCompiledInstruction.from_decoded(
                        item
                    ),
                    obj.instructions,
                )
            ),
            address_table_lookups=list(
                map(
                    lambda item: multisig_message_address_table_lookup.MultisigMessageAddressTableLookup.from_decoded(
                        item
                    ),
                    obj.address_table_lookups,
                )
            ),
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "num_signers": self.num_signers,
            "num_writable_signers": self.num_writable_signers,
            "num_writable_non_signers": self.num_writable_non_signers,
            "account_keys": self.account_keys,
            "instructions": list(
                map(lambda item: item.to_encodable(), self.instructions)
            ),
            "address_table_lookups": list(
                map(lambda item: item.to_encodable(), self.address_table_lookups)
            ),
        }

    def to_json(self) -> VaultTransactionMessageJSON:
        return {
            "num_signers": self.num_signers,
            "num_writable_signers": self.num_writable_signers,
            "num_writable_non_signers": self.num_writable_non_signers,
            "account_keys": list(map(lambda item: str(item), self.account_keys)),
            "instructions": list(map(lambda item: item.to_json(), self.instructions)),
            "address_table_lookups": list(
                map(lambda item: item.to_json(), self.address_table_lookups)
            ),
        }

    @classmethod
    def from_json(cls, obj: VaultTransactionMessageJSON) -> "VaultTransactionMessage":
        return cls(
            num_signers=obj["num_signers"],
            num_writable_signers=obj["num_writable_signers"],
            num_writable_non_signers=obj["num_writable_non_signers"],
            account_keys=list(
                map(lambda item: Pubkey.from_string(item), obj["account_keys"])
            ),
            instructions=list(
                map(
                    lambda item: multisig_compiled_instruction.MultisigCompiledInstruction.from_json(
                        item
                    ),
                    obj["instructions"],
                )
            ),
            address_table_lookups=list(
                map(
                    lambda item: multisig_message_address_table_lookup.MultisigMessageAddressTableLookup.from_json(
                        item
                    ),
                    obj["address_table_lookups"],
                )
            ),
        )
