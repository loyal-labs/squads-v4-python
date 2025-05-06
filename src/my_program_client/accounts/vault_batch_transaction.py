import typing
from dataclasses import dataclass
from solders.pubkey import Pubkey
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Commitment
import borsh_construct as borsh
from anchorpy.coder.accounts import ACCOUNT_DISCRIMINATOR_SIZE
from anchorpy.error import AccountInvalidDiscriminator
from anchorpy.utils.rpc import get_multiple_accounts
from ..program_id import PROGRAM_ID
from .. import types


class VaultBatchTransactionJSON(typing.TypedDict):
    bump: int
    ephemeral_signer_bumps: list[int]
    message: types.vault_transaction_message.VaultTransactionMessageJSON


@dataclass
class VaultBatchTransaction:
    discriminator: typing.ClassVar = b"\xc4y.$\x0c\x13\xfc\x07"
    layout: typing.ClassVar = borsh.CStruct(
        "bump" / borsh.U8,
        "ephemeral_signer_bumps" / borsh.Bytes,
        "message" / types.vault_transaction_message.VaultTransactionMessage.layout,
    )
    bump: int
    ephemeral_signer_bumps: bytes
    message: types.vault_transaction_message.VaultTransactionMessage

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["VaultBatchTransaction"]:
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
    ) -> typing.List[typing.Optional["VaultBatchTransaction"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["VaultBatchTransaction"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "VaultBatchTransaction":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator(
                "The discriminator for this account is invalid"
            )
        dec = VaultBatchTransaction.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            bump=dec.bump,
            ephemeral_signer_bumps=dec.ephemeral_signer_bumps,
            message=types.vault_transaction_message.VaultTransactionMessage.from_decoded(
                dec.message
            ),
        )

    def to_json(self) -> VaultBatchTransactionJSON:
        return {
            "bump": self.bump,
            "ephemeral_signer_bumps": list(self.ephemeral_signer_bumps),
            "message": self.message.to_json(),
        }

    @classmethod
    def from_json(cls, obj: VaultBatchTransactionJSON) -> "VaultBatchTransaction":
        return cls(
            bump=obj["bump"],
            ephemeral_signer_bumps=bytes(obj["ephemeral_signer_bumps"]),
            message=types.vault_transaction_message.VaultTransactionMessage.from_json(
                obj["message"]
            ),
        )
