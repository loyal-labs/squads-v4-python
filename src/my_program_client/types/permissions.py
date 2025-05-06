from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class PermissionsJSON(typing.TypedDict):
    mask: int


@dataclass
class Permissions:
    layout: typing.ClassVar = borsh.CStruct("mask" / borsh.U8)
    mask: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "Permissions":
        return cls(mask=obj.mask)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"mask": self.mask}

    def to_json(self) -> PermissionsJSON:
        return {"mask": self.mask}

    @classmethod
    def from_json(cls, obj: PermissionsJSON) -> "Permissions":
        return cls(mask=obj["mask"])
