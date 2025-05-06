from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class TransactionBufferCreateArgs(typing.TypedDict):
    args: types.transaction_buffer_create_args.TransactionBufferCreateArgs


layout = borsh.CStruct(
    "args" / types.transaction_buffer_create_args.TransactionBufferCreateArgs.layout
)


class TransactionBufferCreateAccounts(typing.TypedDict):
    multisig: Pubkey
    transaction_buffer: Pubkey
    creator: Pubkey
    rent_payer: Pubkey


def transaction_buffer_create(
    args: TransactionBufferCreateArgs,
    accounts: TransactionBufferCreateAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["multisig"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["transaction_buffer"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["creator"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=accounts["rent_payer"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xf5\xc9ql%?\x1dY"
    encoded_args = layout.build(
        {
            "args": args["args"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
