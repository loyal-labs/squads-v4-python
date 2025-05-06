from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh


class MultisigSetRentCollectorArgsJSON(typing.TypedDict):
    rent_collector: typing.Optional[str]
    memo: typing.Optional[str]


@dataclass
class MultisigSetRentCollectorArgs:
    layout: typing.ClassVar = borsh.CStruct(
        "rent_collector" / borsh.Option(BorshPubkey),
        "memo" / borsh.Option(borsh.String),
    )
    rent_collector: typing.Optional[Pubkey]
    memo: typing.Optional[str]

    @classmethod
    def from_decoded(cls, obj: Container) -> "MultisigSetRentCollectorArgs":
        return cls(rent_collector=obj.rent_collector, memo=obj.memo)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"rent_collector": self.rent_collector, "memo": self.memo}

    def to_json(self) -> MultisigSetRentCollectorArgsJSON:
        return {
            "rent_collector": (
                None if self.rent_collector is None else str(self.rent_collector)
            ),
            "memo": self.memo,
        }

    @classmethod
    def from_json(
        cls, obj: MultisigSetRentCollectorArgsJSON
    ) -> "MultisigSetRentCollectorArgs":
        return cls(
            rent_collector=(
                None
                if obj["rent_collector"] is None
                else Pubkey.from_string(obj["rent_collector"])
            ),
            memo=obj["memo"],
        )
