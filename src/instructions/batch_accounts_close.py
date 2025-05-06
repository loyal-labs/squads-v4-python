from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
from ..program_id import PROGRAM_ID


class BatchAccountsCloseAccounts(typing.TypedDict):
    multisig: Pubkey
    proposal: Pubkey
    batch: Pubkey
    rent_collector: Pubkey


def batch_accounts_close(
    accounts: BatchAccountsCloseAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["multisig"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["proposal"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["batch"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["rent_collector"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xda\xc4\x07\xaf\x82f\x0b\xff"
    encoded_args = b""
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
