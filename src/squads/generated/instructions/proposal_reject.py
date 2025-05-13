from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class ProposalRejectArgs(typing.TypedDict):
    args: types.proposal_vote_args.ProposalVoteArgs


layout = borsh.CStruct("args" / types.proposal_vote_args.ProposalVoteArgs.layout)


class ProposalRejectAccounts(typing.TypedDict):
    multisig: Pubkey
    member: Pubkey
    proposal: Pubkey


def proposal_reject(
    args: ProposalRejectArgs,
    accounts: ProposalRejectAccounts,
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
    identifier = b"\xf3>\x86\x9c\xe6j\xf6\x87"
    encoded_args = layout.build(
        {
            "args": args["args"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
