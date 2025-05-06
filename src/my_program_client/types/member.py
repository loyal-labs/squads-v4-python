from __future__ import annotations
from . import (
    permissions,
)
import typing
from dataclasses import dataclass
from construct import Container
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh


class MemberJSON(typing.TypedDict):
    key: str
    permissions: permissions.PermissionsJSON


@dataclass
class Member:
    layout: typing.ClassVar = borsh.CStruct(
        "key" / BorshPubkey, "permissions" / permissions.Permissions.layout
    )
    key: Pubkey
    permissions: permissions.Permissions

    @classmethod
    def from_decoded(cls, obj: Container) -> "Member":
        return cls(
            key=obj.key,
            permissions=permissions.Permissions.from_decoded(obj.permissions),
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"key": self.key, "permissions": self.permissions.to_encodable()}

    def to_json(self) -> MemberJSON:
        return {"key": str(self.key), "permissions": self.permissions.to_json()}

    @classmethod
    def from_json(cls, obj: MemberJSON) -> "Member":
        return cls(
            key=Pubkey.from_string(obj["key"]),
            permissions=permissions.Permissions.from_json(obj["permissions"]),
        )
