from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from spl.token.constants import TOKEN_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class SpendingLimitUseArgs(typing.TypedDict):
    args: types.spending_limit_use_args.SpendingLimitUseArgs


layout = borsh.CStruct(
    "args" / types.spending_limit_use_args.SpendingLimitUseArgs.layout
)


class SpendingLimitUseAccounts(typing.TypedDict):
    multisig: Pubkey
    member: Pubkey
    spending_limit: Pubkey
    vault: Pubkey
    destination: Pubkey
    mint: typing.Optional[Pubkey]
    vault_token_account: typing.Optional[Pubkey]
    destination_token_account: typing.Optional[Pubkey]


def spending_limit_use(
    args: SpendingLimitUseArgs,
    accounts: SpendingLimitUseAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["multisig"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["member"], is_signer=True, is_writable=False),
        AccountMeta(
            pubkey=accounts["spending_limit"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["vault"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["destination"], is_signer=False, is_writable=True),
        (
            AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False)
            if SYS_PROGRAM_ID
            else AccountMeta(pubkey=program_id, is_signer=False, is_writable=False)
        ),
        (
            AccountMeta(pubkey=accounts["mint"], is_signer=False, is_writable=False)
            if accounts["mint"]
            else AccountMeta(pubkey=program_id, is_signer=False, is_writable=False)
        ),
        (
            AccountMeta(
                pubkey=accounts["vault_token_account"],
                is_signer=False,
                is_writable=True,
            )
            if accounts["vault_token_account"]
            else AccountMeta(pubkey=program_id, is_signer=False, is_writable=False)
        ),
        (
            AccountMeta(
                pubkey=accounts["destination_token_account"],
                is_signer=False,
                is_writable=True,
            )
            if accounts["destination_token_account"]
            else AccountMeta(pubkey=program_id, is_signer=False, is_writable=False)
        ),
        (
            AccountMeta(pubkey=TOKEN_PROGRAM_ID, is_signer=False, is_writable=False)
            if TOKEN_PROGRAM_ID
            else AccountMeta(pubkey=program_id, is_signer=False, is_writable=False)
        ),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\x109\x82\x7f\xc1\x14\x9b\x86"
    encoded_args = layout.build(
        {
            "args": args["args"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
