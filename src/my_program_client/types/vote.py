from __future__ import annotations
import typing
from dataclasses import dataclass
from anchorpy.borsh_extension import EnumForCodegen
import borsh_construct as borsh


class ApproveJSON(typing.TypedDict):
    kind: typing.Literal["Approve"]


class RejectJSON(typing.TypedDict):
    kind: typing.Literal["Reject"]


class CancelJSON(typing.TypedDict):
    kind: typing.Literal["Cancel"]


@dataclass
class Approve:
    discriminator: typing.ClassVar = 0
    kind: typing.ClassVar = "Approve"

    @classmethod
    def to_json(cls) -> ApproveJSON:
        return ApproveJSON(
            kind="Approve",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Approve": {},
        }


@dataclass
class Reject:
    discriminator: typing.ClassVar = 1
    kind: typing.ClassVar = "Reject"

    @classmethod
    def to_json(cls) -> RejectJSON:
        return RejectJSON(
            kind="Reject",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Reject": {},
        }


@dataclass
class Cancel:
    discriminator: typing.ClassVar = 2
    kind: typing.ClassVar = "Cancel"

    @classmethod
    def to_json(cls) -> CancelJSON:
        return CancelJSON(
            kind="Cancel",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Cancel": {},
        }


VoteKind = typing.Union[Approve, Reject, Cancel]
VoteJSON = typing.Union[ApproveJSON, RejectJSON, CancelJSON]


def from_decoded(obj: dict) -> VoteKind:
    if not isinstance(obj, dict):
        raise ValueError("Invalid enum object")
    if "Approve" in obj:
        return Approve()
    if "Reject" in obj:
        return Reject()
    if "Cancel" in obj:
        return Cancel()
    raise ValueError("Invalid enum object")


def from_json(obj: VoteJSON) -> VoteKind:
    if obj["kind"] == "Approve":
        return Approve()
    if obj["kind"] == "Reject":
        return Reject()
    if obj["kind"] == "Cancel":
        return Cancel()
    kind = obj["kind"]
    raise ValueError(f"Unrecognized enum kind: {kind}")


layout = EnumForCodegen(
    "Approve" / borsh.CStruct(), "Reject" / borsh.CStruct(), "Cancel" / borsh.CStruct()
)
