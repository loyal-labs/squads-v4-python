from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh


class ProgramConfigSetTreasuryArgsJSON(typing.TypedDict):
    new_treasury: str


@dataclass
class ProgramConfigSetTreasuryArgs:
    layout: typing.ClassVar = borsh.CStruct("new_treasury" / BorshPubkey)
    new_treasury: Pubkey

    @classmethod
    def from_decoded(cls, obj: Container) -> "ProgramConfigSetTreasuryArgs":
        return cls(new_treasury=obj.new_treasury)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"new_treasury": self.new_treasury}

    def to_json(self) -> ProgramConfigSetTreasuryArgsJSON:
        return {"new_treasury": str(self.new_treasury)}

    @classmethod
    def from_json(
        cls, obj: ProgramConfigSetTreasuryArgsJSON
    ) -> "ProgramConfigSetTreasuryArgs":
        return cls(new_treasury=Pubkey.from_string(obj["new_treasury"]))
