from __future__ import annotations
import typing
from dataclasses import dataclass
from anchorpy.borsh_extension import EnumForCodegen
import borsh_construct as borsh


class OneTimeJSON(typing.TypedDict):
    kind: typing.Literal["OneTime"]


class DayJSON(typing.TypedDict):
    kind: typing.Literal["Day"]


class WeekJSON(typing.TypedDict):
    kind: typing.Literal["Week"]


class MonthJSON(typing.TypedDict):
    kind: typing.Literal["Month"]


@dataclass
class OneTime:
    discriminator: typing.ClassVar = 0
    kind: typing.ClassVar = "OneTime"

    @classmethod
    def to_json(cls) -> OneTimeJSON:
        return OneTimeJSON(
            kind="OneTime",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "OneTime": {},
        }


@dataclass
class Day:
    discriminator: typing.ClassVar = 1
    kind: typing.ClassVar = "Day"

    @classmethod
    def to_json(cls) -> DayJSON:
        return DayJSON(
            kind="Day",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Day": {},
        }


@dataclass
class Week:
    discriminator: typing.ClassVar = 2
    kind: typing.ClassVar = "Week"

    @classmethod
    def to_json(cls) -> WeekJSON:
        return WeekJSON(
            kind="Week",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Week": {},
        }


@dataclass
class Month:
    discriminator: typing.ClassVar = 3
    kind: typing.ClassVar = "Month"

    @classmethod
    def to_json(cls) -> MonthJSON:
        return MonthJSON(
            kind="Month",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Month": {},
        }


PeriodKind = typing.Union[OneTime, Day, Week, Month]
PeriodJSON = typing.Union[OneTimeJSON, DayJSON, WeekJSON, MonthJSON]


def from_decoded(obj: dict) -> PeriodKind:
    if not isinstance(obj, dict):
        raise ValueError("Invalid enum object")
    if "OneTime" in obj:
        return OneTime()
    if "Day" in obj:
        return Day()
    if "Week" in obj:
        return Week()
    if "Month" in obj:
        return Month()
    raise ValueError("Invalid enum object")


def from_json(obj: PeriodJSON) -> PeriodKind:
    if obj["kind"] == "OneTime":
        return OneTime()
    if obj["kind"] == "Day":
        return Day()
    if obj["kind"] == "Week":
        return Week()
    if obj["kind"] == "Month":
        return Month()
    kind = obj["kind"]
    raise ValueError(f"Unrecognized enum kind: {kind}")


layout = EnumForCodegen(
    "OneTime" / borsh.CStruct(),
    "Day" / borsh.CStruct(),
    "Week" / borsh.CStruct(),
    "Month" / borsh.CStruct(),
)
