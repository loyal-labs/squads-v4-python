from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class MultisigRemoveSpendingLimitArgs(typing.TypedDict):
    args: types.multisig_remove_spending_limit_args.MultisigRemoveSpendingLimitArgs


layout = borsh.CStruct(
    "args"
    / types.multisig_remove_spending_limit_args.MultisigRemoveSpendingLimitArgs.layout
)


class MultisigRemoveSpendingLimitAccounts(typing.TypedDict):
    multisig: Pubkey
    config_authority: Pubkey
    spending_limit: Pubkey
    rent_collector: Pubkey


def multisig_remove_spending_limit(
    args: MultisigRemoveSpendingLimitArgs,
    accounts: MultisigRemoveSpendingLimitAccounts,
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
        AccountMeta(
            pubkey=accounts["rent_collector"], is_signer=False, is_writable=True
        ),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xe4\xc6\x88o{\x04\xb2q"
    encoded_args = layout.build(
        {
            "args": args["args"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
