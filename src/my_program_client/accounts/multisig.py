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


class MultisigJSON(typing.TypedDict):
    create_key: str
    config_authority: str
    threshold: int
    time_lock: int
    transaction_index: int
    stale_transaction_index: int
    rent_collector: typing.Optional[str]
    bump: int
    members: list[types.member.MemberJSON]


@dataclass
class Multisig:
    discriminator: typing.ClassVar = b"\xe0ty\xbaD\xa1O\xec"
    layout: typing.ClassVar = borsh.CStruct(
        "create_key" / BorshPubkey,
        "config_authority" / BorshPubkey,
        "threshold" / borsh.U16,
        "time_lock" / borsh.U32,
        "transaction_index" / borsh.U64,
        "stale_transaction_index" / borsh.U64,
        "rent_collector" / borsh.Option(BorshPubkey),
        "bump" / borsh.U8,
        "members" / borsh.Vec(typing.cast(Construct, types.member.Member.layout)),
    )
    create_key: Pubkey
    config_authority: Pubkey
    threshold: int
    time_lock: int
    transaction_index: int
    stale_transaction_index: int
    rent_collector: typing.Optional[Pubkey]
    bump: int
    members: list[types.member.Member]

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["Multisig"]:
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
    ) -> typing.List[typing.Optional["Multisig"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["Multisig"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "Multisig":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator(
                "The discriminator for this account is invalid"
            )
        dec = Multisig.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            create_key=dec.create_key,
            config_authority=dec.config_authority,
            threshold=dec.threshold,
            time_lock=dec.time_lock,
            transaction_index=dec.transaction_index,
            stale_transaction_index=dec.stale_transaction_index,
            rent_collector=dec.rent_collector,
            bump=dec.bump,
            members=list(
                map(lambda item: types.member.Member.from_decoded(item), dec.members)
            ),
        )

    def to_json(self) -> MultisigJSON:
        return {
            "create_key": str(self.create_key),
            "config_authority": str(self.config_authority),
            "threshold": self.threshold,
            "time_lock": self.time_lock,
            "transaction_index": self.transaction_index,
            "stale_transaction_index": self.stale_transaction_index,
            "rent_collector": (
                None if self.rent_collector is None else str(self.rent_collector)
            ),
            "bump": self.bump,
            "members": list(map(lambda item: item.to_json(), self.members)),
        }

    @classmethod
    def from_json(cls, obj: MultisigJSON) -> "Multisig":
        return cls(
            create_key=Pubkey.from_string(obj["create_key"]),
            config_authority=Pubkey.from_string(obj["config_authority"]),
            threshold=obj["threshold"],
            time_lock=obj["time_lock"],
            transaction_index=obj["transaction_index"],
            stale_transaction_index=obj["stale_transaction_index"],
            rent_collector=(
                None
                if obj["rent_collector"] is None
                else Pubkey.from_string(obj["rent_collector"])
            ),
            bump=obj["bump"],
            members=list(
                map(lambda item: types.member.Member.from_json(item), obj["members"])
            ),
        )
