from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh


class MultisigSetConfigAuthorityArgsJSON(typing.TypedDict):
    config_authority: str
    memo: typing.Optional[str]


@dataclass
class MultisigSetConfigAuthorityArgs:
    layout: typing.ClassVar = borsh.CStruct(
        "config_authority" / BorshPubkey, "memo" / borsh.Option(borsh.String)
    )
    config_authority: Pubkey
    memo: typing.Optional[str]

    @classmethod
    def from_decoded(cls, obj: Container) -> "MultisigSetConfigAuthorityArgs":
        return cls(config_authority=obj.config_authority, memo=obj.memo)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"config_authority": self.config_authority, "memo": self.memo}

    def to_json(self) -> MultisigSetConfigAuthorityArgsJSON:
        return {"config_authority": str(self.config_authority), "memo": self.memo}

    @classmethod
    def from_json(
        cls, obj: MultisigSetConfigAuthorityArgsJSON
    ) -> "MultisigSetConfigAuthorityArgs":
        return cls(
            config_authority=Pubkey.from_string(obj["config_authority"]),
            memo=obj["memo"],
        )
