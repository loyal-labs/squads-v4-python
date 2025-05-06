from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class TransactionBufferExtendArgs(typing.TypedDict):
    args: types.transaction_buffer_extend_args.TransactionBufferExtendArgs


layout = borsh.CStruct(
    "args" / types.transaction_buffer_extend_args.TransactionBufferExtendArgs.layout
)


class TransactionBufferExtendAccounts(typing.TypedDict):
    multisig: Pubkey
    transaction_buffer: Pubkey
    creator: Pubkey


def transaction_buffer_extend(
    args: TransactionBufferExtendArgs,
    accounts: TransactionBufferExtendAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["multisig"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["transaction_buffer"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["creator"], is_signer=True, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xe6\x9dC8\x05\xee\xf5\x92"
    encoded_args = layout.build(
        {
            "args": args["args"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
