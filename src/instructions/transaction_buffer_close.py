from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
from ..program_id import PROGRAM_ID


class TransactionBufferCloseAccounts(typing.TypedDict):
    multisig: Pubkey
    transaction_buffer: Pubkey
    creator: Pubkey


def transaction_buffer_close(
    accounts: TransactionBufferCloseAccounts,
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
    identifier = b"\x11\xb6\xd0\xe4\x88\x18\xb2f"
    encoded_args = b""
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
