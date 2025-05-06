from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class ProgramConfigSetMultisigCreationFeeArgsJSON(typing.TypedDict):
    new_multisig_creation_fee: int


@dataclass
class ProgramConfigSetMultisigCreationFeeArgs:
    layout: typing.ClassVar = borsh.CStruct("new_multisig_creation_fee" / borsh.U64)
    new_multisig_creation_fee: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "ProgramConfigSetMultisigCreationFeeArgs":
        return cls(new_multisig_creation_fee=obj.new_multisig_creation_fee)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"new_multisig_creation_fee": self.new_multisig_creation_fee}

    def to_json(self) -> ProgramConfigSetMultisigCreationFeeArgsJSON:
        return {"new_multisig_creation_fee": self.new_multisig_creation_fee}

    @classmethod
    def from_json(
        cls, obj: ProgramConfigSetMultisigCreationFeeArgsJSON
    ) -> "ProgramConfigSetMultisigCreationFeeArgs":
        return cls(new_multisig_creation_fee=obj["new_multisig_creation_fee"])
