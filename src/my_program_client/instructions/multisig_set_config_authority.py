from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class MultisigSetConfigAuthorityArgs(typing.TypedDict):
    args: types.multisig_set_config_authority_args.MultisigSetConfigAuthorityArgs


layout = borsh.CStruct(
    "args"
    / types.multisig_set_config_authority_args.MultisigSetConfigAuthorityArgs.layout
)


class MultisigSetConfigAuthorityAccounts(typing.TypedDict):
    multisig: Pubkey
    config_authority: Pubkey
    rent_payer: typing.Optional[Pubkey]


def multisig_set_config_authority(
    args: MultisigSetConfigAuthorityArgs,
    accounts: MultisigSetConfigAuthorityAccounts,
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
    identifier = b"\x8f]\xc7\x8f\\\xa9\xc1\xe8"
    encoded_args = layout.build(
        {
            "args": args["args"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
