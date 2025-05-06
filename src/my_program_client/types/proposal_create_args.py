from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class ProposalCreateArgsJSON(typing.TypedDict):
    transaction_index: int
    draft: bool


@dataclass
class ProposalCreateArgs:
    layout: typing.ClassVar = borsh.CStruct(
        "transaction_index" / borsh.U64, "draft" / borsh.Bool
    )
    transaction_index: int
    draft: bool

    @classmethod
    def from_decoded(cls, obj: Container) -> "ProposalCreateArgs":
        return cls(transaction_index=obj.transaction_index, draft=obj.draft)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"transaction_index": self.transaction_index, "draft": self.draft}

    def to_json(self) -> ProposalCreateArgsJSON:
        return {"transaction_index": self.transaction_index, "draft": self.draft}

    @classmethod
    def from_json(cls, obj: ProposalCreateArgsJSON) -> "ProposalCreateArgs":
        return cls(transaction_index=obj["transaction_index"], draft=obj["draft"])
