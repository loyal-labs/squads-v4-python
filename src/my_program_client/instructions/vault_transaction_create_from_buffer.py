from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class VaultTransactionCreateFromBufferArgs(typing.TypedDict):
    args: types.vault_transaction_create_args.VaultTransactionCreateArgs


layout = borsh.CStruct(
    "args" / types.vault_transaction_create_args.VaultTransactionCreateArgs.layout
)


class VaultTransactionCreateFromBufferAccounts(typing.TypedDict):
    vault_transaction_create: VaultTransactionCreateNested
    transaction_buffer: Pubkey
    creator: Pubkey


class VaultTransactionCreateNested(typing.TypedDict):
    multisig: Pubkey
    transaction: Pubkey
    creator: Pubkey
    rent_payer: Pubkey


def vault_transaction_create_from_buffer(
    args: VaultTransactionCreateFromBufferArgs,
    accounts: VaultTransactionCreateFromBufferAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(
            pubkey=accounts["vault_transaction_create"]["multisig"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["vault_transaction_create"]["transaction"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["vault_transaction_create"]["creator"],
            is_signer=True,
            is_writable=False,
        ),
        AccountMeta(
            pubkey=accounts["vault_transaction_create"]["rent_payer"],
            is_signer=True,
            is_writable=True,
        ),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["transaction_buffer"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["creator"], is_signer=True, is_writable=True),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xde6\x95DW\xf60\xe7"
    encoded_args = layout.build(
        {
            "args": args["args"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
