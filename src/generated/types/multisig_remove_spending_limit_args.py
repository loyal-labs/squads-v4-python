from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class MultisigRemoveSpendingLimitArgsJSON(typing.TypedDict):
    memo: typing.Optional[str]


@dataclass
class MultisigRemoveSpendingLimitArgs:
    layout: typing.ClassVar = borsh.CStruct("memo" / borsh.Option(borsh.String))
    memo: typing.Optional[str]

    @classmethod
    def from_decoded(cls, obj: Container) -> "MultisigRemoveSpendingLimitArgs":
        return cls(memo=obj.memo)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"memo": self.memo}

    def to_json(self) -> MultisigRemoveSpendingLimitArgsJSON:
        return {"memo": self.memo}

    @classmethod
    def from_json(
        cls, obj: MultisigRemoveSpendingLimitArgsJSON
    ) -> "MultisigRemoveSpendingLimitArgs":
        return cls(memo=obj["memo"])
