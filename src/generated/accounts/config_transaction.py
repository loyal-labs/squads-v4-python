import typing
from dataclasses import dataclass
from construct import Construct
from solders.pubkey import Pubkey
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Commitment
import borsh_construct as borsh
from anchorpy.coder.accounts import ACCOUNT_DISCRIMINATOR_SIZE
from anchorpy.error import AccountInvalidDiscriminator
from anchorpy.utils.rpc import get_multiple_accounts
from anchorpy.borsh_extension import BorshPubkey
from ..program_id import PROGRAM_ID
from .. import types


class ConfigTransactionJSON(typing.TypedDict):
    multisig: str
    creator: str
    index: int
    bump: int
    actions: list[types.config_action.ConfigActionJSON]


@dataclass
class ConfigTransaction:
    discriminator: typing.ClassVar = b"^\x08\x04#q\x8b\x8bp"
    layout: typing.ClassVar = borsh.CStruct(
        "multisig" / BorshPubkey,
        "creator" / BorshPubkey,
        "index" / borsh.U64,
        "bump" / borsh.U8,
        "actions" / borsh.Vec(typing.cast(Construct, types.config_action.layout)),
    )
    multisig: Pubkey
    creator: Pubkey
    index: int
    bump: int
    actions: list[types.config_action.ConfigActionKind]

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["ConfigTransaction"]:
        resp = await conn.get_account_info(address, commitment=commitment)
        info = resp.value
        if info is None:
            return None
        if info.owner != program_id:
            raise ValueError("Account does not belong to this program")
        bytes_data = info.data
        return cls.decode(bytes_data)

    @classmethod
    async def fetch_multiple(
        cls,
        conn: AsyncClient,
        addresses: list[Pubkey],
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.List[typing.Optional["ConfigTransaction"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["ConfigTransaction"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "ConfigTransaction":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator(
                "The discriminator for this account is invalid"
            )
        dec = ConfigTransaction.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            multisig=dec.multisig,
            creator=dec.creator,
            index=dec.index,
            bump=dec.bump,
            actions=list(
                map(lambda item: types.config_action.from_decoded(item), dec.actions)
            ),
        )

    def to_json(self) -> ConfigTransactionJSON:
        return {
            "multisig": str(self.multisig),
            "creator": str(self.creator),
            "index": self.index,
            "bump": self.bump,
            "actions": list(map(lambda item: item.to_json(), self.actions)),
        }

    @classmethod
    def from_json(cls, obj: ConfigTransactionJSON) -> "ConfigTransaction":
        return cls(
            multisig=Pubkey.from_string(obj["multisig"]),
            creator=Pubkey.from_string(obj["creator"]),
            index=obj["index"],
            bump=obj["bump"],
            actions=list(
                map(lambda item: types.config_action.from_json(item), obj["actions"])
            ),
        )
