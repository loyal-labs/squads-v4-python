from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class BatchCreateArgsJSON(typing.TypedDict):
    vault_index: int
    memo: typing.Optional[str]


@dataclass
class BatchCreateArgs:
    layout: typing.ClassVar = borsh.CStruct(
        "vault_index" / borsh.U8, "memo" / borsh.Option(borsh.String)
    )
    vault_index: int
    memo: typing.Optional[str]

    @classmethod
    def from_decoded(cls, obj: Container) -> "BatchCreateArgs":
        return cls(vault_index=obj.vault_index, memo=obj.memo)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"vault_index": self.vault_index, "memo": self.memo}

    def to_json(self) -> BatchCreateArgsJSON:
        return {"vault_index": self.vault_index, "memo": self.memo}

    @classmethod
    def from_json(cls, obj: BatchCreateArgsJSON) -> "BatchCreateArgs":
        return cls(vault_index=obj["vault_index"], memo=obj["memo"])
