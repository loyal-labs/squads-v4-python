from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class MultisigSetTimeLockArgsJSON(typing.TypedDict):
    time_lock: int
    memo: typing.Optional[str]


@dataclass
class MultisigSetTimeLockArgs:
    layout: typing.ClassVar = borsh.CStruct(
        "time_lock" / borsh.U32, "memo" / borsh.Option(borsh.String)
    )
    time_lock: int
    memo: typing.Optional[str]

    @classmethod
    def from_decoded(cls, obj: Container) -> "MultisigSetTimeLockArgs":
        return cls(time_lock=obj.time_lock, memo=obj.memo)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"time_lock": self.time_lock, "memo": self.memo}

    def to_json(self) -> MultisigSetTimeLockArgsJSON:
        return {"time_lock": self.time_lock, "memo": self.memo}

    @classmethod
    def from_json(cls, obj: MultisigSetTimeLockArgsJSON) -> "MultisigSetTimeLockArgs":
        return cls(time_lock=obj["time_lock"], memo=obj["memo"])
