from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
from ..program_id import PROGRAM_ID


class MultisigCreateAccounts(typing.TypedDict):
    null: Pubkey


def multisig_create(
    accounts: MultisigCreateAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["null"], is_signer=False, is_writable=False)
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"zMP\x9fTXZ\xc5"
    encoded_args = b""
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
