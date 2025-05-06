from __future__ import annotations
from . import (
    period,
)
import typing
from dataclasses import dataclass
from construct import Container, Construct
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh


class MultisigAddSpendingLimitArgsJSON(typing.TypedDict):
    create_key: str
    vault_index: int
    mint: str
    amount: int
    period: period.PeriodJSON
    members: list[str]
    destinations: list[str]
    memo: typing.Optional[str]


@dataclass
class MultisigAddSpendingLimitArgs:
    layout: typing.ClassVar = borsh.CStruct(
        "create_key" / BorshPubkey,
        "vault_index" / borsh.U8,
        "mint" / BorshPubkey,
        "amount" / borsh.U64,
        "period" / period.layout,
        "members" / borsh.Vec(typing.cast(Construct, BorshPubkey)),
        "destinations" / borsh.Vec(typing.cast(Construct, BorshPubkey)),
        "memo" / borsh.Option(borsh.String),
    )
    create_key: Pubkey
    vault_index: int
    mint: Pubkey
    amount: int
    period: period.PeriodKind
    members: list[Pubkey]
    destinations: list[Pubkey]
    memo: typing.Optional[str]

    @classmethod
    def from_decoded(cls, obj: Container) -> "MultisigAddSpendingLimitArgs":
        return cls(
            create_key=obj.create_key,
            vault_index=obj.vault_index,
            mint=obj.mint,
            amount=obj.amount,
            period=period.from_decoded(obj.period),
            members=obj.members,
            destinations=obj.destinations,
            memo=obj.memo,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "create_key": self.create_key,
            "vault_index": self.vault_index,
            "mint": self.mint,
            "amount": self.amount,
            "period": self.period.to_encodable(),
            "members": self.members,
            "destinations": self.destinations,
            "memo": self.memo,
        }

    def to_json(self) -> MultisigAddSpendingLimitArgsJSON:
        return {
            "create_key": str(self.create_key),
            "vault_index": self.vault_index,
            "mint": str(self.mint),
            "amount": self.amount,
            "period": self.period.to_json(),
            "members": list(map(lambda item: str(item), self.members)),
            "destinations": list(map(lambda item: str(item), self.destinations)),
            "memo": self.memo,
        }

    @classmethod
    def from_json(
        cls, obj: MultisigAddSpendingLimitArgsJSON
    ) -> "MultisigAddSpendingLimitArgs":
        return cls(
            create_key=Pubkey.from_string(obj["create_key"]),
            vault_index=obj["vault_index"],
            mint=Pubkey.from_string(obj["mint"]),
            amount=obj["amount"],
            period=period.from_json(obj["period"]),
            members=list(map(lambda item: Pubkey.from_string(item), obj["members"])),
            destinations=list(
                map(lambda item: Pubkey.from_string(item), obj["destinations"])
            ),
            memo=obj["memo"],
        )
