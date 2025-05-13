from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class ProposalVoteArgsJSON(typing.TypedDict):
    memo: typing.Optional[str]


@dataclass
class ProposalVoteArgs:
    layout: typing.ClassVar = borsh.CStruct("memo" / borsh.Option(borsh.String))
    memo: typing.Optional[str]

    @classmethod
    def from_decoded(cls, obj: Container) -> "ProposalVoteArgs":
        return cls(memo=obj.memo)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"memo": self.memo}

    def to_json(self) -> ProposalVoteArgsJSON:
        return {"memo": self.memo}

    @classmethod
    def from_json(cls, obj: ProposalVoteArgsJSON) -> "ProposalVoteArgs":
        return cls(memo=obj["memo"])
