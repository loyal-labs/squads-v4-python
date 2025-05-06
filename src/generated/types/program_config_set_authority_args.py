from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh


class ProgramConfigSetAuthorityArgsJSON(typing.TypedDict):
    new_authority: str


@dataclass
class ProgramConfigSetAuthorityArgs:
    layout: typing.ClassVar = borsh.CStruct("new_authority" / BorshPubkey)
    new_authority: Pubkey

    @classmethod
    def from_decoded(cls, obj: Container) -> "ProgramConfigSetAuthorityArgs":
        return cls(new_authority=obj.new_authority)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"new_authority": self.new_authority}

    def to_json(self) -> ProgramConfigSetAuthorityArgsJSON:
        return {"new_authority": str(self.new_authority)}

    @classmethod
    def from_json(
        cls, obj: ProgramConfigSetAuthorityArgsJSON
    ) -> "ProgramConfigSetAuthorityArgs":
        return cls(new_authority=Pubkey.from_string(obj["new_authority"]))
