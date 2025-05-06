from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
from ..program_id import PROGRAM_ID


class VaultBatchTransactionAccountCloseAccounts(typing.TypedDict):
    multisig: Pubkey
    proposal: Pubkey
    batch: Pubkey
    transaction: Pubkey
    rent_collector: Pubkey


def vault_batch_transaction_account_close(
    accounts: VaultBatchTransactionAccountCloseAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["multisig"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["proposal"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["batch"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["transaction"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["rent_collector"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\x86\x12\x13j\x81Da\xf7"
    encoded_args = b""
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
