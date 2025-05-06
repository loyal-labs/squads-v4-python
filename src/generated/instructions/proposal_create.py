from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class ProposalCreateArgs(typing.TypedDict):
    args: types.proposal_create_args.ProposalCreateArgs


layout = borsh.CStruct("args" / types.proposal_create_args.ProposalCreateArgs.layout)


class ProposalCreateAccounts(typing.TypedDict):
    multisig: Pubkey
    proposal: Pubkey
    creator: Pubkey
    rent_payer: Pubkey


def proposal_create(
    args: ProposalCreateArgs,
    accounts: ProposalCreateAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["multisig"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["proposal"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["creator"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=accounts["rent_payer"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xdc<I\xe0\x1elO\x9f"
    encoded_args = layout.build(
        {
            "args": args["args"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
