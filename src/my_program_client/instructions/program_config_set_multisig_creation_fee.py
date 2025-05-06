from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class ProgramConfigSetMultisigCreationFeeArgs(typing.TypedDict):
    args: (
        types.program_config_set_multisig_creation_fee_args.ProgramConfigSetMultisigCreationFeeArgs
    )


layout = borsh.CStruct(
    "args"
    / types.program_config_set_multisig_creation_fee_args.ProgramConfigSetMultisigCreationFeeArgs.layout
)


class ProgramConfigSetMultisigCreationFeeAccounts(typing.TypedDict):
    program_config: Pubkey
    authority: Pubkey


def program_config_set_multisig_creation_fee(
    args: ProgramConfigSetMultisigCreationFeeArgs,
    accounts: ProgramConfigSetMultisigCreationFeeAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(
            pubkey=accounts["program_config"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"e\xa0\xf9?\x9a\xd7\x99\r"
    encoded_args = layout.build(
        {
            "args": args["args"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
