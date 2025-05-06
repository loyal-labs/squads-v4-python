from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class MultisigChangeThresholdArgsJSON(typing.TypedDict):
    new_threshold: int
    memo: typing.Optional[str]


@dataclass
class MultisigChangeThresholdArgs:
    layout: typing.ClassVar = borsh.CStruct(
        "new_threshold" / borsh.U16, "memo" / borsh.Option(borsh.String)
    )
    new_threshold: int
    memo: typing.Optional[str]

    @classmethod
    def from_decoded(cls, obj: Container) -> "MultisigChangeThresholdArgs":
        return cls(new_threshold=obj.new_threshold, memo=obj.memo)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"new_threshold": self.new_threshold, "memo": self.memo}

    def to_json(self) -> MultisigChangeThresholdArgsJSON:
        return {"new_threshold": self.new_threshold, "memo": self.memo}

    @classmethod
    def from_json(
        cls, obj: MultisigChangeThresholdArgsJSON
    ) -> "MultisigChangeThresholdArgs":
        return cls(new_threshold=obj["new_threshold"], memo=obj["memo"])
