from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
from ..program_id import PROGRAM_ID


class ProposalActivateAccounts(typing.TypedDict):
    multisig: Pubkey
    member: Pubkey
    proposal: Pubkey


def proposal_activate(
    accounts: ProposalActivateAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["multisig"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["member"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["proposal"], is_signer=False, is_writable=True),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b'\x0b"\\\xf8\x9a\x1b3j'
    encoded_args = b""
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
