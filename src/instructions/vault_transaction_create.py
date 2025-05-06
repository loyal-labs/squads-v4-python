from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class VaultTransactionCreateArgs(typing.TypedDict):
    args: types.vault_transaction_create_args.VaultTransactionCreateArgs


layout = borsh.CStruct(
    "args" / types.vault_transaction_create_args.VaultTransactionCreateArgs.layout
)


class VaultTransactionCreateAccounts(typing.TypedDict):
    multisig: Pubkey
    transaction: Pubkey
    creator: Pubkey
    rent_payer: Pubkey


def vault_transaction_create(
    args: VaultTransactionCreateArgs,
    accounts: VaultTransactionCreateAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["multisig"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["transaction"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["creator"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=accounts["rent_payer"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"0\xfaN\xa8\xd0\xe2\xda\xd3"
    encoded_args = layout.build(
        {
            "args": args["args"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
