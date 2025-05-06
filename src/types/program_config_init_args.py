from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh


class ProgramConfigInitArgsJSON(typing.TypedDict):
    authority: str
    multisig_creation_fee: int
    treasury: str


@dataclass
class ProgramConfigInitArgs:
    layout: typing.ClassVar = borsh.CStruct(
        "authority" / BorshPubkey,
        "multisig_creation_fee" / borsh.U64,
        "treasury" / BorshPubkey,
    )
    authority: Pubkey
    multisig_creation_fee: int
    treasury: Pubkey

    @classmethod
    def from_decoded(cls, obj: Container) -> "ProgramConfigInitArgs":
        return cls(
            authority=obj.authority,
            multisig_creation_fee=obj.multisig_creation_fee,
            treasury=obj.treasury,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "authority": self.authority,
            "multisig_creation_fee": self.multisig_creation_fee,
            "treasury": self.treasury,
        }

    def to_json(self) -> ProgramConfigInitArgsJSON:
        return {
            "authority": str(self.authority),
            "multisig_creation_fee": self.multisig_creation_fee,
            "treasury": str(self.treasury),
        }

    @classmethod
    def from_json(cls, obj: ProgramConfigInitArgsJSON) -> "ProgramConfigInitArgs":
        return cls(
            authority=Pubkey.from_string(obj["authority"]),
            multisig_creation_fee=obj["multisig_creation_fee"],
            treasury=Pubkey.from_string(obj["treasury"]),
        )
