from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh


class MultisigRemoveMemberArgsJSON(typing.TypedDict):
    old_member: str
    memo: typing.Optional[str]


@dataclass
class MultisigRemoveMemberArgs:
    layout: typing.ClassVar = borsh.CStruct(
        "old_member" / BorshPubkey, "memo" / borsh.Option(borsh.String)
    )
    old_member: Pubkey
    memo: typing.Optional[str]

    @classmethod
    def from_decoded(cls, obj: Container) -> "MultisigRemoveMemberArgs":
        return cls(old_member=obj.old_member, memo=obj.memo)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"old_member": self.old_member, "memo": self.memo}

    def to_json(self) -> MultisigRemoveMemberArgsJSON:
        return {"old_member": str(self.old_member), "memo": self.memo}

    @classmethod
    def from_json(cls, obj: MultisigRemoveMemberArgsJSON) -> "MultisigRemoveMemberArgs":
        return cls(old_member=Pubkey.from_string(obj["old_member"]), memo=obj["memo"])
