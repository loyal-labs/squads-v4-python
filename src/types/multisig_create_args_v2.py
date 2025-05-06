from __future__ import annotations
from . import (
    member,
)
import typing
from dataclasses import dataclass
from construct import Container, Construct
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh


class MultisigCreateArgsV2JSON(typing.TypedDict):
    config_authority: typing.Optional[str]
    threshold: int
    members: list[member.MemberJSON]
    time_lock: int
    rent_collector: typing.Optional[str]
    memo: typing.Optional[str]


@dataclass
class MultisigCreateArgsV2:
    layout: typing.ClassVar = borsh.CStruct(
        "config_authority" / borsh.Option(BorshPubkey),
        "threshold" / borsh.U16,
        "members" / borsh.Vec(typing.cast(Construct, member.Member.layout)),
        "time_lock" / borsh.U32,
        "rent_collector" / borsh.Option(BorshPubkey),
        "memo" / borsh.Option(borsh.String),
    )
    config_authority: typing.Optional[Pubkey]
    threshold: int
    members: list[member.Member]
    time_lock: int
    rent_collector: typing.Optional[Pubkey]
    memo: typing.Optional[str]

    @classmethod
    def from_decoded(cls, obj: Container) -> "MultisigCreateArgsV2":
        return cls(
            config_authority=obj.config_authority,
            threshold=obj.threshold,
            members=list(
                map(lambda item: member.Member.from_decoded(item), obj.members)
            ),
            time_lock=obj.time_lock,
            rent_collector=obj.rent_collector,
            memo=obj.memo,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "config_authority": self.config_authority,
            "threshold": self.threshold,
            "members": list(map(lambda item: item.to_encodable(), self.members)),
            "time_lock": self.time_lock,
            "rent_collector": self.rent_collector,
            "memo": self.memo,
        }

    def to_json(self) -> MultisigCreateArgsV2JSON:
        return {
            "config_authority": (
                None if self.config_authority is None else str(self.config_authority)
            ),
            "threshold": self.threshold,
            "members": list(map(lambda item: item.to_json(), self.members)),
            "time_lock": self.time_lock,
            "rent_collector": (
                None if self.rent_collector is None else str(self.rent_collector)
            ),
            "memo": self.memo,
        }

    @classmethod
    def from_json(cls, obj: MultisigCreateArgsV2JSON) -> "MultisigCreateArgsV2":
        return cls(
            config_authority=(
                None
                if obj["config_authority"] is None
                else Pubkey.from_string(obj["config_authority"])
            ),
            threshold=obj["threshold"],
            members=list(
                map(lambda item: member.Member.from_json(item), obj["members"])
            ),
            time_lock=obj["time_lock"],
            rent_collector=(
                None
                if obj["rent_collector"] is None
                else Pubkey.from_string(obj["rent_collector"])
            ),
            memo=obj["memo"],
        )
