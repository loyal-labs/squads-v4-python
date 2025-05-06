from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class ProgramConfigSetTreasuryArgs(typing.TypedDict):
    args: types.program_config_set_treasury_args.ProgramConfigSetTreasuryArgs


layout = borsh.CStruct(
    "args" / types.program_config_set_treasury_args.ProgramConfigSetTreasuryArgs.layout
)


class ProgramConfigSetTreasuryAccounts(typing.TypedDict):
    program_config: Pubkey
    authority: Pubkey


def program_config_set_treasury(
    args: ProgramConfigSetTreasuryArgs,
    accounts: ProgramConfigSetTreasuryAccounts,
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
    identifier = b"o.\xf3u\x90\xbc\xa2k"
    encoded_args = layout.build(
        {
            "args": args["args"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
