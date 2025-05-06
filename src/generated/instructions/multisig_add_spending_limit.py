from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class MultisigAddSpendingLimitArgs(typing.TypedDict):
    args: types.multisig_add_spending_limit_args.MultisigAddSpendingLimitArgs


layout = borsh.CStruct(
    "args" / types.multisig_add_spending_limit_args.MultisigAddSpendingLimitArgs.layout
)


class MultisigAddSpendingLimitAccounts(typing.TypedDict):
    multisig: Pubkey
    config_authority: Pubkey
    spending_limit: Pubkey
    rent_payer: Pubkey


def multisig_add_spending_limit(
    args: MultisigAddSpendingLimitArgs,
    accounts: MultisigAddSpendingLimitAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["multisig"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["config_authority"], is_signer=True, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["spending_limit"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["rent_payer"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\x0b\xf2\x9f*V\xc5Ys"
    encoded_args = layout.build(
        {
            "args": args["args"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
