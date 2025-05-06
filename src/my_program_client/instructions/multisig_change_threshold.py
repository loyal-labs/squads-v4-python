from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class MultisigChangeThresholdArgs(typing.TypedDict):
    args: types.multisig_change_threshold_args.MultisigChangeThresholdArgs


layout = borsh.CStruct(
    "args" / types.multisig_change_threshold_args.MultisigChangeThresholdArgs.layout
)


class MultisigChangeThresholdAccounts(typing.TypedDict):
    multisig: Pubkey
    config_authority: Pubkey
    rent_payer: typing.Optional[Pubkey]


def multisig_change_threshold(
    args: MultisigChangeThresholdArgs,
    accounts: MultisigChangeThresholdAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["multisig"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["config_authority"], is_signer=True, is_writable=False
        ),
        (
            AccountMeta(pubkey=accounts["rent_payer"], is_signer=True, is_writable=True)
            if accounts["rent_payer"]
            else AccountMeta(pubkey=program_id, is_signer=False, is_writable=False)
        ),
        (
            AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False)
            if SYS_PROGRAM_ID
            else AccountMeta(pubkey=program_id, is_signer=False, is_writable=False)
        ),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\x8d*\x0f~\xa9\\>\xb5"
    encoded_args = layout.build(
        {
            "args": args["args"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
