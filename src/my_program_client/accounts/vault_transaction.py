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
from .. import types


class VaultTransactionJSON(typing.TypedDict):
    multisig: str
    creator: str
    index: int
    bump: int
    vault_index: int
    vault_bump: int
    ephemeral_signer_bumps: list[int]
    message: types.vault_transaction_message.VaultTransactionMessageJSON


@dataclass
class VaultTransaction:
    discriminator: typing.ClassVar = b"\xa8\xfa\xa2dQ\x0e\xa2\xcf"
    layout: typing.ClassVar = borsh.CStruct(
        "multisig" / BorshPubkey,
        "creator" / BorshPubkey,
        "index" / borsh.U64,
        "bump" / borsh.U8,
        "vault_index" / borsh.U8,
        "vault_bump" / borsh.U8,
        "ephemeral_signer_bumps" / borsh.Bytes,
        "message" / types.vault_transaction_message.VaultTransactionMessage.layout,
    )
    multisig: Pubkey
    creator: Pubkey
    index: int
    bump: int
    vault_index: int
    vault_bump: int
    ephemeral_signer_bumps: bytes
    message: types.vault_transaction_message.VaultTransactionMessage

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["VaultTransaction"]:
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
    ) -> typing.List[typing.Optional["VaultTransaction"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["VaultTransaction"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "VaultTransaction":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator(
                "The discriminator for this account is invalid"
            )
        dec = VaultTransaction.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            multisig=dec.multisig,
            creator=dec.creator,
            index=dec.index,
            bump=dec.bump,
            vault_index=dec.vault_index,
            vault_bump=dec.vault_bump,
            ephemeral_signer_bumps=dec.ephemeral_signer_bumps,
            message=types.vault_transaction_message.VaultTransactionMessage.from_decoded(
                dec.message
            ),
        )

    def to_json(self) -> VaultTransactionJSON:
        return {
            "multisig": str(self.multisig),
            "creator": str(self.creator),
            "index": self.index,
            "bump": self.bump,
            "vault_index": self.vault_index,
            "vault_bump": self.vault_bump,
            "ephemeral_signer_bumps": list(self.ephemeral_signer_bumps),
            "message": self.message.to_json(),
        }

    @classmethod
    def from_json(cls, obj: VaultTransactionJSON) -> "VaultTransaction":
        return cls(
            multisig=Pubkey.from_string(obj["multisig"]),
            creator=Pubkey.from_string(obj["creator"]),
            index=obj["index"],
            bump=obj["bump"],
            vault_index=obj["vault_index"],
            vault_bump=obj["vault_bump"],
            ephemeral_signer_bumps=bytes(obj["ephemeral_signer_bumps"]),
            message=types.vault_transaction_message.VaultTransactionMessage.from_json(
                obj["message"]
            ),
        )
