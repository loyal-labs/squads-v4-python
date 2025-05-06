from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class BatchAddTransactionArgs(typing.TypedDict):
    args: types.batch_add_transaction_args.BatchAddTransactionArgs


layout = borsh.CStruct(
    "args" / types.batch_add_transaction_args.BatchAddTransactionArgs.layout
)


class BatchAddTransactionAccounts(typing.TypedDict):
    multisig: Pubkey
    proposal: Pubkey
    batch: Pubkey
    transaction: Pubkey
    member: Pubkey
    rent_payer: Pubkey


def batch_add_transaction(
    args: BatchAddTransactionArgs,
    accounts: BatchAddTransactionAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["multisig"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["proposal"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["batch"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["transaction"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["member"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=accounts["rent_payer"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"Yd\xe0\x12EF6L"
    encoded_args = layout.build(
        {
            "args": args["args"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
