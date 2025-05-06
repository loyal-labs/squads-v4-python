from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
from ..program_id import PROGRAM_ID


class VaultTransactionExecuteAccounts(typing.TypedDict):
    multisig: Pubkey
    proposal: Pubkey
    transaction: Pubkey
    member: Pubkey


def vault_transaction_execute(
    accounts: VaultTransactionExecuteAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["multisig"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["proposal"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["transaction"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["member"], is_signer=True, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xc2\x08\xa1W\x99\xa4\x19\xab"
    encoded_args = b""
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
