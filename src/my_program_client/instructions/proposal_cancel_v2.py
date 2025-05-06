from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class ProposalCancelV2Args(typing.TypedDict):
    args: types.proposal_vote_args.ProposalVoteArgs


layout = borsh.CStruct("args" / types.proposal_vote_args.ProposalVoteArgs.layout)


class ProposalCancelV2Accounts(typing.TypedDict):
    proposal_vote: ProposalVoteNested


class ProposalVoteNested(typing.TypedDict):
    multisig: Pubkey
    member: Pubkey
    proposal: Pubkey


def proposal_cancel_v2(
    args: ProposalCancelV2Args,
    accounts: ProposalCancelV2Accounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(
            pubkey=accounts["proposal_vote"]["multisig"],
            is_signer=False,
            is_writable=False,
        ),
        AccountMeta(
            pubkey=accounts["proposal_vote"]["member"], is_signer=True, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["proposal_vote"]["proposal"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xcd)\xc2=\xdc\x8b\x10\xf7"
    encoded_args = layout.build(
        {
            "args": args["args"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
