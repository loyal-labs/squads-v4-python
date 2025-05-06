from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class BatchCreateArgs(typing.TypedDict):
    args: types.batch_create_args.BatchCreateArgs


layout = borsh.CStruct("args" / types.batch_create_args.BatchCreateArgs.layout)


class BatchCreateAccounts(typing.TypedDict):
    multisig: Pubkey
    batch: Pubkey
    creator: Pubkey
    rent_payer: Pubkey


def batch_create(
    args: BatchCreateArgs,
    accounts: BatchCreateAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["multisig"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["batch"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["creator"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=accounts["rent_payer"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xc2\x8e\x8d\x117\xb9\x14\xf8"
    encoded_args = layout.build(
        {
            "args": args["args"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
