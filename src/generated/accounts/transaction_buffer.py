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


class TransactionBufferJSON(typing.TypedDict):
    multisig: str
    creator: str
    buffer_index: int
    vault_index: int
    final_buffer_hash: list[int]
    final_buffer_size: int
    buffer: list[int]


@dataclass
class TransactionBuffer:
    discriminator: typing.ClassVar = b"Z$#\xdb]\xe1n`"
    layout: typing.ClassVar = borsh.CStruct(
        "multisig" / BorshPubkey,
        "creator" / BorshPubkey,
        "buffer_index" / borsh.U8,
        "vault_index" / borsh.U8,
        "final_buffer_hash" / borsh.U8[32],
        "final_buffer_size" / borsh.U16,
        "buffer" / borsh.Bytes,
    )
    multisig: Pubkey
    creator: Pubkey
    buffer_index: int
    vault_index: int
    final_buffer_hash: list[int]
    final_buffer_size: int
    buffer: bytes

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["TransactionBuffer"]:
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
    ) -> typing.List[typing.Optional["TransactionBuffer"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["TransactionBuffer"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "TransactionBuffer":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator(
                "The discriminator for this account is invalid"
            )
        dec = TransactionBuffer.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            multisig=dec.multisig,
            creator=dec.creator,
            buffer_index=dec.buffer_index,
            vault_index=dec.vault_index,
            final_buffer_hash=dec.final_buffer_hash,
            final_buffer_size=dec.final_buffer_size,
            buffer=dec.buffer,
        )

    def to_json(self) -> TransactionBufferJSON:
        return {
            "multisig": str(self.multisig),
            "creator": str(self.creator),
            "buffer_index": self.buffer_index,
            "vault_index": self.vault_index,
            "final_buffer_hash": self.final_buffer_hash,
            "final_buffer_size": self.final_buffer_size,
            "buffer": list(self.buffer),
        }

    @classmethod
    def from_json(cls, obj: TransactionBufferJSON) -> "TransactionBuffer":
        return cls(
            multisig=Pubkey.from_string(obj["multisig"]),
            creator=Pubkey.from_string(obj["creator"]),
            buffer_index=obj["buffer_index"],
            vault_index=obj["vault_index"],
            final_buffer_hash=obj["final_buffer_hash"],
            final_buffer_size=obj["final_buffer_size"],
            buffer=bytes(obj["buffer"]),
        )
