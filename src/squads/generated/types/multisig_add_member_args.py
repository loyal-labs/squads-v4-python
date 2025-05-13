from __future__ import annotations
from . import (
    member,
)
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class MultisigAddMemberArgsJSON(typing.TypedDict):
    new_member: member.MemberJSON
    memo: typing.Optional[str]


@dataclass
class MultisigAddMemberArgs:
    layout: typing.ClassVar = borsh.CStruct(
        "new_member" / member.Member.layout, "memo" / borsh.Option(borsh.String)
    )
    new_member: member.Member
    memo: typing.Optional[str]

    @classmethod
    def from_decoded(cls, obj: Container) -> "MultisigAddMemberArgs":
        return cls(new_member=member.Member.from_decoded(obj.new_member), memo=obj.memo)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"new_member": self.new_member.to_encodable(), "memo": self.memo}

    def to_json(self) -> MultisigAddMemberArgsJSON:
        return {"new_member": self.new_member.to_json(), "memo": self.memo}

    @classmethod
    def from_json(cls, obj: MultisigAddMemberArgsJSON) -> "MultisigAddMemberArgs":
        return cls(
            new_member=member.Member.from_json(obj["new_member"]), memo=obj["memo"]
        )
