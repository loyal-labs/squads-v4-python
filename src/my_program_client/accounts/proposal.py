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


class ProposalJSON(typing.TypedDict):
    multisig: str
    transaction_index: int
    status: types.proposal_status.ProposalStatusJSON
    bump: int
    approved: list[str]
    rejected: list[str]
    cancelled: list[str]


@dataclass
class Proposal:
    discriminator: typing.ClassVar = b"\x1a^\xbd\xbbt\x885!"
    layout: typing.ClassVar = borsh.CStruct(
        "multisig" / BorshPubkey,
        "transaction_index" / borsh.U64,
        "status" / types.proposal_status.layout,
        "bump" / borsh.U8,
        "approved" / borsh.Vec(typing.cast(Construct, BorshPubkey)),
        "rejected" / borsh.Vec(typing.cast(Construct, BorshPubkey)),
        "cancelled" / borsh.Vec(typing.cast(Construct, BorshPubkey)),
    )
    multisig: Pubkey
    transaction_index: int
    status: types.proposal_status.ProposalStatusKind
    bump: int
    approved: list[Pubkey]
    rejected: list[Pubkey]
    cancelled: list[Pubkey]

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["Proposal"]:
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
    ) -> typing.List[typing.Optional["Proposal"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["Proposal"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "Proposal":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator(
                "The discriminator for this account is invalid"
            )
        dec = Proposal.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            multisig=dec.multisig,
            transaction_index=dec.transaction_index,
            status=types.proposal_status.from_decoded(dec.status),
            bump=dec.bump,
            approved=dec.approved,
            rejected=dec.rejected,
            cancelled=dec.cancelled,
        )

    def to_json(self) -> ProposalJSON:
        return {
            "multisig": str(self.multisig),
            "transaction_index": self.transaction_index,
            "status": self.status.to_json(),
            "bump": self.bump,
            "approved": list(map(lambda item: str(item), self.approved)),
            "rejected": list(map(lambda item: str(item), self.rejected)),
            "cancelled": list(map(lambda item: str(item), self.cancelled)),
        }

    @classmethod
    def from_json(cls, obj: ProposalJSON) -> "Proposal":
        return cls(
            multisig=Pubkey.from_string(obj["multisig"]),
            transaction_index=obj["transaction_index"],
            status=types.proposal_status.from_json(obj["status"]),
            bump=obj["bump"],
            approved=list(map(lambda item: Pubkey.from_string(item), obj["approved"])),
            rejected=list(map(lambda item: Pubkey.from_string(item), obj["rejected"])),
            cancelled=list(
                map(lambda item: Pubkey.from_string(item), obj["cancelled"])
            ),
        )
