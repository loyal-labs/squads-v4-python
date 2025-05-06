from __future__ import annotations
import typing
from dataclasses import dataclass
from anchorpy.borsh_extension import EnumForCodegen
import borsh_construct as borsh


class DraftJSONValue(typing.TypedDict):
    timestamp: int


class ActiveJSONValue(typing.TypedDict):
    timestamp: int


class RejectedJSONValue(typing.TypedDict):
    timestamp: int


class ApprovedJSONValue(typing.TypedDict):
    timestamp: int


class ExecutedJSONValue(typing.TypedDict):
    timestamp: int


class CancelledJSONValue(typing.TypedDict):
    timestamp: int


class DraftValue(typing.TypedDict):
    timestamp: int


class ActiveValue(typing.TypedDict):
    timestamp: int


class RejectedValue(typing.TypedDict):
    timestamp: int


class ApprovedValue(typing.TypedDict):
    timestamp: int


class ExecutedValue(typing.TypedDict):
    timestamp: int


class CancelledValue(typing.TypedDict):
    timestamp: int


class DraftJSON(typing.TypedDict):
    value: DraftJSONValue
    kind: typing.Literal["Draft"]


class ActiveJSON(typing.TypedDict):
    value: ActiveJSONValue
    kind: typing.Literal["Active"]


class RejectedJSON(typing.TypedDict):
    value: RejectedJSONValue
    kind: typing.Literal["Rejected"]


class ApprovedJSON(typing.TypedDict):
    value: ApprovedJSONValue
    kind: typing.Literal["Approved"]


class ExecutingJSON(typing.TypedDict):
    kind: typing.Literal["Executing"]


class ExecutedJSON(typing.TypedDict):
    value: ExecutedJSONValue
    kind: typing.Literal["Executed"]


class CancelledJSON(typing.TypedDict):
    value: CancelledJSONValue
    kind: typing.Literal["Cancelled"]


@dataclass
class Draft:
    discriminator: typing.ClassVar = 0
    kind: typing.ClassVar = "Draft"
    value: DraftValue

    def to_json(self) -> DraftJSON:
        return DraftJSON(
            kind="Draft",
            value={
                "timestamp": self.value["timestamp"],
            },
        )

    def to_encodable(self) -> dict:
        return {
            "Draft": {
                "timestamp": self.value["timestamp"],
            },
        }


@dataclass
class Active:
    discriminator: typing.ClassVar = 1
    kind: typing.ClassVar = "Active"
    value: ActiveValue

    def to_json(self) -> ActiveJSON:
        return ActiveJSON(
            kind="Active",
            value={
                "timestamp": self.value["timestamp"],
            },
        )

    def to_encodable(self) -> dict:
        return {
            "Active": {
                "timestamp": self.value["timestamp"],
            },
        }


@dataclass
class Rejected:
    discriminator: typing.ClassVar = 2
    kind: typing.ClassVar = "Rejected"
    value: RejectedValue

    def to_json(self) -> RejectedJSON:
        return RejectedJSON(
            kind="Rejected",
            value={
                "timestamp": self.value["timestamp"],
            },
        )

    def to_encodable(self) -> dict:
        return {
            "Rejected": {
                "timestamp": self.value["timestamp"],
            },
        }


@dataclass
class Approved:
    discriminator: typing.ClassVar = 3
    kind: typing.ClassVar = "Approved"
    value: ApprovedValue

    def to_json(self) -> ApprovedJSON:
        return ApprovedJSON(
            kind="Approved",
            value={
                "timestamp": self.value["timestamp"],
            },
        )

    def to_encodable(self) -> dict:
        return {
            "Approved": {
                "timestamp": self.value["timestamp"],
            },
        }


@dataclass
class Executing:
    discriminator: typing.ClassVar = 4
    kind: typing.ClassVar = "Executing"

    @classmethod
    def to_json(cls) -> ExecutingJSON:
        return ExecutingJSON(
            kind="Executing",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Executing": {},
        }


@dataclass
class Executed:
    discriminator: typing.ClassVar = 5
    kind: typing.ClassVar = "Executed"
    value: ExecutedValue

    def to_json(self) -> ExecutedJSON:
        return ExecutedJSON(
            kind="Executed",
            value={
                "timestamp": self.value["timestamp"],
            },
        )

    def to_encodable(self) -> dict:
        return {
            "Executed": {
                "timestamp": self.value["timestamp"],
            },
        }


@dataclass
class Cancelled:
    discriminator: typing.ClassVar = 6
    kind: typing.ClassVar = "Cancelled"
    value: CancelledValue

    def to_json(self) -> CancelledJSON:
        return CancelledJSON(
            kind="Cancelled",
            value={
                "timestamp": self.value["timestamp"],
            },
        )

    def to_encodable(self) -> dict:
        return {
            "Cancelled": {
                "timestamp": self.value["timestamp"],
            },
        }


ProposalStatusKind = typing.Union[
    Draft, Active, Rejected, Approved, Executing, Executed, Cancelled
]
ProposalStatusJSON = typing.Union[
    DraftJSON,
    ActiveJSON,
    RejectedJSON,
    ApprovedJSON,
    ExecutingJSON,
    ExecutedJSON,
    CancelledJSON,
]


def from_decoded(obj: dict) -> ProposalStatusKind:
    if not isinstance(obj, dict):
        raise ValueError("Invalid enum object")
    if "Draft" in obj:
        val = obj["Draft"]
        return Draft(
            DraftValue(
                timestamp=val["timestamp"],
            )
        )
    if "Active" in obj:
        val = obj["Active"]
        return Active(
            ActiveValue(
                timestamp=val["timestamp"],
            )
        )
    if "Rejected" in obj:
        val = obj["Rejected"]
        return Rejected(
            RejectedValue(
                timestamp=val["timestamp"],
            )
        )
    if "Approved" in obj:
        val = obj["Approved"]
        return Approved(
            ApprovedValue(
                timestamp=val["timestamp"],
            )
        )
    if "Executing" in obj:
        return Executing()
    if "Executed" in obj:
        val = obj["Executed"]
        return Executed(
            ExecutedValue(
                timestamp=val["timestamp"],
            )
        )
    if "Cancelled" in obj:
        val = obj["Cancelled"]
        return Cancelled(
            CancelledValue(
                timestamp=val["timestamp"],
            )
        )
    raise ValueError("Invalid enum object")


def from_json(obj: ProposalStatusJSON) -> ProposalStatusKind:
    if obj["kind"] == "Draft":
        draft_json_value = typing.cast(DraftJSONValue, obj["value"])
        return Draft(
            DraftValue(
                timestamp=draft_json_value["timestamp"],
            )
        )
    if obj["kind"] == "Active":
        active_json_value = typing.cast(ActiveJSONValue, obj["value"])
        return Active(
            ActiveValue(
                timestamp=active_json_value["timestamp"],
            )
        )
    if obj["kind"] == "Rejected":
        rejected_json_value = typing.cast(RejectedJSONValue, obj["value"])
        return Rejected(
            RejectedValue(
                timestamp=rejected_json_value["timestamp"],
            )
        )
    if obj["kind"] == "Approved":
        approved_json_value = typing.cast(ApprovedJSONValue, obj["value"])
        return Approved(
            ApprovedValue(
                timestamp=approved_json_value["timestamp"],
            )
        )
    if obj["kind"] == "Executing":
        return Executing()
    if obj["kind"] == "Executed":
        executed_json_value = typing.cast(ExecutedJSONValue, obj["value"])
        return Executed(
            ExecutedValue(
                timestamp=executed_json_value["timestamp"],
            )
        )
    if obj["kind"] == "Cancelled":
        cancelled_json_value = typing.cast(CancelledJSONValue, obj["value"])
        return Cancelled(
            CancelledValue(
                timestamp=cancelled_json_value["timestamp"],
            )
        )
    kind = obj["kind"]
    raise ValueError(f"Unrecognized enum kind: {kind}")


layout = EnumForCodegen(
    "Draft" / borsh.CStruct("timestamp" / borsh.I64),
    "Active" / borsh.CStruct("timestamp" / borsh.I64),
    "Rejected" / borsh.CStruct("timestamp" / borsh.I64),
    "Approved" / borsh.CStruct("timestamp" / borsh.I64),
    "Executing" / borsh.CStruct(),
    "Executed" / borsh.CStruct("timestamp" / borsh.I64),
    "Cancelled" / borsh.CStruct("timestamp" / borsh.I64),
)
