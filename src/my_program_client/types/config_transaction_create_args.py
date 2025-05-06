from __future__ import annotations
from . import (
    config_action,
)
import typing
from dataclasses import dataclass
from construct import Container, Construct
import borsh_construct as borsh


class ConfigTransactionCreateArgsJSON(typing.TypedDict):
    actions: list[config_action.ConfigActionJSON]
    memo: typing.Optional[str]


@dataclass
class ConfigTransactionCreateArgs:
    layout: typing.ClassVar = borsh.CStruct(
        "actions" / borsh.Vec(typing.cast(Construct, config_action.layout)),
        "memo" / borsh.Option(borsh.String),
    )
    actions: list[config_action.ConfigActionKind]
    memo: typing.Optional[str]

    @classmethod
    def from_decoded(cls, obj: Container) -> "ConfigTransactionCreateArgs":
        return cls(
            actions=list(
                map(lambda item: config_action.from_decoded(item), obj.actions)
            ),
            memo=obj.memo,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "actions": list(map(lambda item: item.to_encodable(), self.actions)),
            "memo": self.memo,
        }

    def to_json(self) -> ConfigTransactionCreateArgsJSON:
        return {
            "actions": list(map(lambda item: item.to_json(), self.actions)),
            "memo": self.memo,
        }

    @classmethod
    def from_json(
        cls, obj: ConfigTransactionCreateArgsJSON
    ) -> "ConfigTransactionCreateArgs":
        return cls(
            actions=list(
                map(lambda item: config_action.from_json(item), obj["actions"])
            ),
            memo=obj["memo"],
        )
