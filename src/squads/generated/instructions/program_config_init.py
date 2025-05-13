from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class ProgramConfigInitArgs(typing.TypedDict):
    args: types.program_config_init_args.ProgramConfigInitArgs


layout = borsh.CStruct(
    "args" / types.program_config_init_args.ProgramConfigInitArgs.layout
)


class ProgramConfigInitAccounts(typing.TypedDict):
    program_config: Pubkey
    initializer: Pubkey


def program_config_init(
    args: ProgramConfigInitArgs,
    accounts: ProgramConfigInitAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(
            pubkey=accounts["program_config"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["initializer"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xb8\xbc\xc6\xc3\xcd|u\xd8"
    encoded_args = layout.build(
        {
            "args": args["args"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
