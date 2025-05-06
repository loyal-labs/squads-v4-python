from __future__ import annotations
from . import (
    member,
    period,
)
import typing
from dataclasses import dataclass
from solders.pubkey import Pubkey
from construct import Construct
from anchorpy.borsh_extension import EnumForCodegen, BorshPubkey
import borsh_construct as borsh


class AddMemberJSONValue(typing.TypedDict):
    new_member: member.MemberJSON


class RemoveMemberJSONValue(typing.TypedDict):
    old_member: str


class ChangeThresholdJSONValue(typing.TypedDict):
    new_threshold: int


class SetTimeLockJSONValue(typing.TypedDict):
    new_time_lock: int


class AddSpendingLimitJSONValue(typing.TypedDict):
    create_key: str
    vault_index: int
    mint: str
    amount: int
    period: period.PeriodJSON
    members: list[str]
    destinations: list[str]


class RemoveSpendingLimitJSONValue(typing.TypedDict):
    spending_limit: str


class SetRentCollectorJSONValue(typing.TypedDict):
    new_rent_collector: typing.Optional[str]


class AddMemberValue(typing.TypedDict):
    new_member: member.Member


class RemoveMemberValue(typing.TypedDict):
    old_member: Pubkey


class ChangeThresholdValue(typing.TypedDict):
    new_threshold: int


class SetTimeLockValue(typing.TypedDict):
    new_time_lock: int


class AddSpendingLimitValue(typing.TypedDict):
    create_key: Pubkey
    vault_index: int
    mint: Pubkey
    amount: int
    period: period.PeriodKind
    members: list[Pubkey]
    destinations: list[Pubkey]


class RemoveSpendingLimitValue(typing.TypedDict):
    spending_limit: Pubkey


class SetRentCollectorValue(typing.TypedDict):
    new_rent_collector: typing.Optional[Pubkey]


class AddMemberJSON(typing.TypedDict):
    value: AddMemberJSONValue
    kind: typing.Literal["AddMember"]


class RemoveMemberJSON(typing.TypedDict):
    value: RemoveMemberJSONValue
    kind: typing.Literal["RemoveMember"]


class ChangeThresholdJSON(typing.TypedDict):
    value: ChangeThresholdJSONValue
    kind: typing.Literal["ChangeThreshold"]


class SetTimeLockJSON(typing.TypedDict):
    value: SetTimeLockJSONValue
    kind: typing.Literal["SetTimeLock"]


class AddSpendingLimitJSON(typing.TypedDict):
    value: AddSpendingLimitJSONValue
    kind: typing.Literal["AddSpendingLimit"]


class RemoveSpendingLimitJSON(typing.TypedDict):
    value: RemoveSpendingLimitJSONValue
    kind: typing.Literal["RemoveSpendingLimit"]


class SetRentCollectorJSON(typing.TypedDict):
    value: SetRentCollectorJSONValue
    kind: typing.Literal["SetRentCollector"]


@dataclass
class AddMember:
    discriminator: typing.ClassVar = 0
    kind: typing.ClassVar = "AddMember"
    value: AddMemberValue

    def to_json(self) -> AddMemberJSON:
        return AddMemberJSON(
            kind="AddMember",
            value={
                "new_member": self.value["new_member"].to_json(),
            },
        )

    def to_encodable(self) -> dict:
        return {
            "AddMember": {
                "new_member": self.value["new_member"].to_encodable(),
            },
        }


@dataclass
class RemoveMember:
    discriminator: typing.ClassVar = 1
    kind: typing.ClassVar = "RemoveMember"
    value: RemoveMemberValue

    def to_json(self) -> RemoveMemberJSON:
        return RemoveMemberJSON(
            kind="RemoveMember",
            value={
                "old_member": str(self.value["old_member"]),
            },
        )

    def to_encodable(self) -> dict:
        return {
            "RemoveMember": {
                "old_member": self.value["old_member"],
            },
        }


@dataclass
class ChangeThreshold:
    discriminator: typing.ClassVar = 2
    kind: typing.ClassVar = "ChangeThreshold"
    value: ChangeThresholdValue

    def to_json(self) -> ChangeThresholdJSON:
        return ChangeThresholdJSON(
            kind="ChangeThreshold",
            value={
                "new_threshold": self.value["new_threshold"],
            },
        )

    def to_encodable(self) -> dict:
        return {
            "ChangeThreshold": {
                "new_threshold": self.value["new_threshold"],
            },
        }


@dataclass
class SetTimeLock:
    discriminator: typing.ClassVar = 3
    kind: typing.ClassVar = "SetTimeLock"
    value: SetTimeLockValue

    def to_json(self) -> SetTimeLockJSON:
        return SetTimeLockJSON(
            kind="SetTimeLock",
            value={
                "new_time_lock": self.value["new_time_lock"],
            },
        )

    def to_encodable(self) -> dict:
        return {
            "SetTimeLock": {
                "new_time_lock": self.value["new_time_lock"],
            },
        }


@dataclass
class AddSpendingLimit:
    discriminator: typing.ClassVar = 4
    kind: typing.ClassVar = "AddSpendingLimit"
    value: AddSpendingLimitValue

    def to_json(self) -> AddSpendingLimitJSON:
        return AddSpendingLimitJSON(
            kind="AddSpendingLimit",
            value={
                "create_key": str(self.value["create_key"]),
                "vault_index": self.value["vault_index"],
                "mint": str(self.value["mint"]),
                "amount": self.value["amount"],
                "period": self.value["period"].to_json(),
                "members": list(map(lambda item: str(item), self.value["members"])),
                "destinations": list(
                    map(lambda item: str(item), self.value["destinations"])
                ),
            },
        )

    def to_encodable(self) -> dict:
        return {
            "AddSpendingLimit": {
                "create_key": self.value["create_key"],
                "vault_index": self.value["vault_index"],
                "mint": self.value["mint"],
                "amount": self.value["amount"],
                "period": self.value["period"].to_encodable(),
                "members": self.value["members"],
                "destinations": self.value["destinations"],
            },
        }


@dataclass
class RemoveSpendingLimit:
    discriminator: typing.ClassVar = 5
    kind: typing.ClassVar = "RemoveSpendingLimit"
    value: RemoveSpendingLimitValue

    def to_json(self) -> RemoveSpendingLimitJSON:
        return RemoveSpendingLimitJSON(
            kind="RemoveSpendingLimit",
            value={
                "spending_limit": str(self.value["spending_limit"]),
            },
        )

    def to_encodable(self) -> dict:
        return {
            "RemoveSpendingLimit": {
                "spending_limit": self.value["spending_limit"],
            },
        }


@dataclass
class SetRentCollector:
    discriminator: typing.ClassVar = 6
    kind: typing.ClassVar = "SetRentCollector"
    value: SetRentCollectorValue

    def to_json(self) -> SetRentCollectorJSON:
        return SetRentCollectorJSON(
            kind="SetRentCollector",
            value={
                "new_rent_collector": (
                    None
                    if self.value["new_rent_collector"] is None
                    else str(self.value["new_rent_collector"])
                ),
            },
        )

    def to_encodable(self) -> dict:
        return {
            "SetRentCollector": {
                "new_rent_collector": self.value["new_rent_collector"],
            },
        }


ConfigActionKind = typing.Union[
    AddMember,
    RemoveMember,
    ChangeThreshold,
    SetTimeLock,
    AddSpendingLimit,
    RemoveSpendingLimit,
    SetRentCollector,
]
ConfigActionJSON = typing.Union[
    AddMemberJSON,
    RemoveMemberJSON,
    ChangeThresholdJSON,
    SetTimeLockJSON,
    AddSpendingLimitJSON,
    RemoveSpendingLimitJSON,
    SetRentCollectorJSON,
]


def from_decoded(obj: dict) -> ConfigActionKind:
    if not isinstance(obj, dict):
        raise ValueError("Invalid enum object")
    if "AddMember" in obj:
        val = obj["AddMember"]
        return AddMember(
            AddMemberValue(
                new_member=member.Member.from_decoded(val["new_member"]),
            )
        )
    if "RemoveMember" in obj:
        val = obj["RemoveMember"]
        return RemoveMember(
            RemoveMemberValue(
                old_member=val["old_member"],
            )
        )
    if "ChangeThreshold" in obj:
        val = obj["ChangeThreshold"]
        return ChangeThreshold(
            ChangeThresholdValue(
                new_threshold=val["new_threshold"],
            )
        )
    if "SetTimeLock" in obj:
        val = obj["SetTimeLock"]
        return SetTimeLock(
            SetTimeLockValue(
                new_time_lock=val["new_time_lock"],
            )
        )
    if "AddSpendingLimit" in obj:
        val = obj["AddSpendingLimit"]
        return AddSpendingLimit(
            AddSpendingLimitValue(
                create_key=val["create_key"],
                vault_index=val["vault_index"],
                mint=val["mint"],
                amount=val["amount"],
                period=period.from_decoded(val["period"]),
                members=val["members"],
                destinations=val["destinations"],
            )
        )
    if "RemoveSpendingLimit" in obj:
        val = obj["RemoveSpendingLimit"]
        return RemoveSpendingLimit(
            RemoveSpendingLimitValue(
                spending_limit=val["spending_limit"],
            )
        )
    if "SetRentCollector" in obj:
        val = obj["SetRentCollector"]
        return SetRentCollector(
            SetRentCollectorValue(
                new_rent_collector=val["new_rent_collector"],
            )
        )
    raise ValueError("Invalid enum object")


def from_json(obj: ConfigActionJSON) -> ConfigActionKind:
    if obj["kind"] == "AddMember":
        add_member_json_value = typing.cast(AddMemberJSONValue, obj["value"])
        return AddMember(
            AddMemberValue(
                new_member=member.Member.from_json(add_member_json_value["new_member"]),
            )
        )
    if obj["kind"] == "RemoveMember":
        remove_member_json_value = typing.cast(RemoveMemberJSONValue, obj["value"])
        return RemoveMember(
            RemoveMemberValue(
                old_member=Pubkey.from_string(remove_member_json_value["old_member"]),
            )
        )
    if obj["kind"] == "ChangeThreshold":
        change_threshold_json_value = typing.cast(
            ChangeThresholdJSONValue, obj["value"]
        )
        return ChangeThreshold(
            ChangeThresholdValue(
                new_threshold=change_threshold_json_value["new_threshold"],
            )
        )
    if obj["kind"] == "SetTimeLock":
        set_time_lock_json_value = typing.cast(SetTimeLockJSONValue, obj["value"])
        return SetTimeLock(
            SetTimeLockValue(
                new_time_lock=set_time_lock_json_value["new_time_lock"],
            )
        )
    if obj["kind"] == "AddSpendingLimit":
        add_spending_limit_json_value = typing.cast(
            AddSpendingLimitJSONValue, obj["value"]
        )
        return AddSpendingLimit(
            AddSpendingLimitValue(
                create_key=Pubkey.from_string(
                    add_spending_limit_json_value["create_key"]
                ),
                vault_index=add_spending_limit_json_value["vault_index"],
                mint=Pubkey.from_string(add_spending_limit_json_value["mint"]),
                amount=add_spending_limit_json_value["amount"],
                period=period.from_json(add_spending_limit_json_value["period"]),
                members=list(
                    map(
                        lambda item: Pubkey.from_string(item),
                        add_spending_limit_json_value["members"],
                    )
                ),
                destinations=list(
                    map(
                        lambda item: Pubkey.from_string(item),
                        add_spending_limit_json_value["destinations"],
                    )
                ),
            )
        )
    if obj["kind"] == "RemoveSpendingLimit":
        remove_spending_limit_json_value = typing.cast(
            RemoveSpendingLimitJSONValue, obj["value"]
        )
        return RemoveSpendingLimit(
            RemoveSpendingLimitValue(
                spending_limit=Pubkey.from_string(
                    remove_spending_limit_json_value["spending_limit"]
                ),
            )
        )
    if obj["kind"] == "SetRentCollector":
        set_rent_collector_json_value = typing.cast(
            SetRentCollectorJSONValue, obj["value"]
        )
        return SetRentCollector(
            SetRentCollectorValue(
                new_rent_collector=(
                    None
                    if set_rent_collector_json_value["new_rent_collector"] is None
                    else Pubkey.from_string(
                        set_rent_collector_json_value["new_rent_collector"]
                    )
                ),
            )
        )
    kind = obj["kind"]
    raise ValueError(f"Unrecognized enum kind: {kind}")


layout = EnumForCodegen(
    "AddMember" / borsh.CStruct("new_member" / member.Member.layout),
    "RemoveMember" / borsh.CStruct("old_member" / BorshPubkey),
    "ChangeThreshold" / borsh.CStruct("new_threshold" / borsh.U16),
    "SetTimeLock" / borsh.CStruct("new_time_lock" / borsh.U32),
    "AddSpendingLimit"
    / borsh.CStruct(
        "create_key" / BorshPubkey,
        "vault_index" / borsh.U8,
        "mint" / BorshPubkey,
        "amount" / borsh.U64,
        "period" / period.layout,
        "members" / borsh.Vec(typing.cast(Construct, BorshPubkey)),
        "destinations" / borsh.Vec(typing.cast(Construct, BorshPubkey)),
    ),
    "RemoveSpendingLimit" / borsh.CStruct("spending_limit" / BorshPubkey),
    "SetRentCollector"
    / borsh.CStruct("new_rent_collector" / borsh.Option(BorshPubkey)),
)
