from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class MultisigCreateV2Args(typing.TypedDict):
    args: types.multisig_create_args_v2.MultisigCreateArgsV2


layout = borsh.CStruct(
    "args" / types.multisig_create_args_v2.MultisigCreateArgsV2.layout
)


class MultisigCreateV2Accounts(typing.TypedDict):
    program_config: Pubkey
    treasury: Pubkey
    multisig: Pubkey
    create_key: Pubkey
    creator: Pubkey


def multisig_create_v2(
    args: MultisigCreateV2Args,
    accounts: MultisigCreateV2Accounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(
            pubkey=accounts["program_config"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["treasury"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["multisig"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["create_key"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=accounts["creator"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"2\xdd\xc7](\xf5\x8b\xe9"
    encoded_args = layout.build(
        {
            "args": args["args"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
