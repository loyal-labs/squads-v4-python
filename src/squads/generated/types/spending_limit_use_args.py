from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class SpendingLimitUseArgsJSON(typing.TypedDict):
    amount: int
    decimals: int
    memo: typing.Optional[str]


@dataclass
class SpendingLimitUseArgs:
    layout: typing.ClassVar = borsh.CStruct(
        "amount" / borsh.U64, "decimals" / borsh.U8, "memo" / borsh.Option(borsh.String)
    )
    amount: int
    decimals: int
    memo: typing.Optional[str]

    @classmethod
    def from_decoded(cls, obj: Container) -> "SpendingLimitUseArgs":
        return cls(amount=obj.amount, decimals=obj.decimals, memo=obj.memo)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"amount": self.amount, "decimals": self.decimals, "memo": self.memo}

    def to_json(self) -> SpendingLimitUseArgsJSON:
        return {"amount": self.amount, "decimals": self.decimals, "memo": self.memo}

    @classmethod
    def from_json(cls, obj: SpendingLimitUseArgsJSON) -> "SpendingLimitUseArgs":
        return cls(amount=obj["amount"], decimals=obj["decimals"], memo=obj["memo"])
