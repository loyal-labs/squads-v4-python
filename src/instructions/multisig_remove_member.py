from solders.instruction import Instruction
from solders.pubkey import Pubkey

from src.generated.instructions.multisig_remove_member import (
    MultisigRemoveMemberAccounts,
    MultisigRemoveMemberArgs,
)
from src.generated.instructions.multisig_remove_member import (
    multisig_remove_member as multisig_remove_member_instruction,
)
from src.generated.program_id import PROGRAM_ID
from src.generated.types.multisig_remove_member_args import (
    MultisigRemoveMemberArgs as MultisigRemoveMemberArgsType,
)


def multisig_remove_member(
    multisig_pda: Pubkey,
    config_authority: Pubkey,
    old_member: Pubkey,
    memo: str | None,
    program_id: Pubkey | None,
) -> Instruction:
    if program_id is None:
        program_id = PROGRAM_ID

    try:
        assert isinstance(multisig_pda, Pubkey)
        assert isinstance(config_authority, Pubkey)
        assert isinstance(old_member, Pubkey)
        assert isinstance(memo, str | None)
        assert isinstance(program_id, Pubkey)
    except AssertionError:
        raise ValueError("Invalid argument") from None

    accounts = MultisigRemoveMemberAccounts(
        multisig=multisig_pda,
        config_authority=config_authority,
        rent_payer=None,
    )
    args = MultisigRemoveMemberArgs(
        args=MultisigRemoveMemberArgsType(
            old_member=old_member,
            memo=memo,
        )
    )

    return multisig_remove_member_instruction(
        accounts=accounts, args=args, program_id=program_id
    )
