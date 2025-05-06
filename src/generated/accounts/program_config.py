import typing
from dataclasses import dataclass
from solders.pubkey import Pubkey
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Commitment
import borsh_construct as borsh
from anchorpy.coder.accounts import ACCOUNT_DISCRIMINATOR_SIZE
from anchorpy.error import AccountInvalidDiscriminator
from anchorpy.utils.rpc import get_multiple_accounts
from anchorpy.borsh_extension import BorshPubkey
from ..program_id import PROGRAM_ID


class ProgramConfigJSON(typing.TypedDict):
    authority: str
    multisig_creation_fee: int
    treasury: str
    reserved: list[int]


@dataclass
class ProgramConfig:
    discriminator: typing.ClassVar = b"\xc4\xd2Z\xe7\x90\x95\x8c?"
    layout: typing.ClassVar = borsh.CStruct(
        "authority" / BorshPubkey,
        "multisig_creation_fee" / borsh.U64,
        "treasury" / BorshPubkey,
        "reserved" / borsh.U8[64],
    )
    authority: Pubkey
    multisig_creation_fee: int
    treasury: Pubkey
    reserved: list[int]

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["ProgramConfig"]:
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
    ) -> typing.List[typing.Optional["ProgramConfig"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["ProgramConfig"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "ProgramConfig":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator(
                "The discriminator for this account is invalid"
            )
        dec = ProgramConfig.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            authority=dec.authority,
            multisig_creation_fee=dec.multisig_creation_fee,
            treasury=dec.treasury,
            reserved=dec.reserved,
        )

    def to_json(self) -> ProgramConfigJSON:
        return {
            "authority": str(self.authority),
            "multisig_creation_fee": self.multisig_creation_fee,
            "treasury": str(self.treasury),
            "reserved": self.reserved,
        }

    @classmethod
    def from_json(cls, obj: ProgramConfigJSON) -> "ProgramConfig":
        return cls(
            authority=Pubkey.from_string(obj["authority"]),
            multisig_creation_fee=obj["multisig_creation_fee"],
            treasury=Pubkey.from_string(obj["treasury"]),
            reserved=obj["reserved"],
        )
