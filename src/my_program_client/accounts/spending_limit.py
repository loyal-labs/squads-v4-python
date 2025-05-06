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


class SpendingLimitJSON(typing.TypedDict):
    multisig: str
    create_key: str
    vault_index: int
    mint: str
    amount: int
    period: types.period.PeriodJSON
    remaining_amount: int
    last_reset: int
    bump: int
    members: list[str]
    destinations: list[str]


@dataclass
class SpendingLimit:
    discriminator: typing.ClassVar = b"\n\xc9\x1b\xa0\xda\xc3\xde\x98"
    layout: typing.ClassVar = borsh.CStruct(
        "multisig" / BorshPubkey,
        "create_key" / BorshPubkey,
        "vault_index" / borsh.U8,
        "mint" / BorshPubkey,
        "amount" / borsh.U64,
        "period" / types.period.layout,
        "remaining_amount" / borsh.U64,
        "last_reset" / borsh.I64,
        "bump" / borsh.U8,
        "members" / borsh.Vec(typing.cast(Construct, BorshPubkey)),
        "destinations" / borsh.Vec(typing.cast(Construct, BorshPubkey)),
    )
    multisig: Pubkey
    create_key: Pubkey
    vault_index: int
    mint: Pubkey
    amount: int
    period: types.period.PeriodKind
    remaining_amount: int
    last_reset: int
    bump: int
    members: list[Pubkey]
    destinations: list[Pubkey]

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["SpendingLimit"]:
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
    ) -> typing.List[typing.Optional["SpendingLimit"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["SpendingLimit"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "SpendingLimit":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator(
                "The discriminator for this account is invalid"
            )
        dec = SpendingLimit.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            multisig=dec.multisig,
            create_key=dec.create_key,
            vault_index=dec.vault_index,
            mint=dec.mint,
            amount=dec.amount,
            period=types.period.from_decoded(dec.period),
            remaining_amount=dec.remaining_amount,
            last_reset=dec.last_reset,
            bump=dec.bump,
            members=dec.members,
            destinations=dec.destinations,
        )

    def to_json(self) -> SpendingLimitJSON:
        return {
            "multisig": str(self.multisig),
            "create_key": str(self.create_key),
            "vault_index": self.vault_index,
            "mint": str(self.mint),
            "amount": self.amount,
            "period": self.period.to_json(),
            "remaining_amount": self.remaining_amount,
            "last_reset": self.last_reset,
            "bump": self.bump,
            "members": list(map(lambda item: str(item), self.members)),
            "destinations": list(map(lambda item: str(item), self.destinations)),
        }

    @classmethod
    def from_json(cls, obj: SpendingLimitJSON) -> "SpendingLimit":
        return cls(
            multisig=Pubkey.from_string(obj["multisig"]),
            create_key=Pubkey.from_string(obj["create_key"]),
            vault_index=obj["vault_index"],
            mint=Pubkey.from_string(obj["mint"]),
            amount=obj["amount"],
            period=types.period.from_json(obj["period"]),
            remaining_amount=obj["remaining_amount"],
            last_reset=obj["last_reset"],
            bump=obj["bump"],
            members=list(map(lambda item: Pubkey.from_string(item), obj["members"])),
            destinations=list(
                map(lambda item: Pubkey.from_string(item), obj["destinations"])
            ),
        )
