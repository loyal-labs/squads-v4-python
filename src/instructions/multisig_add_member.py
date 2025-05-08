from solders.instruction import Instruction
from solders.pubkey import Pubkey

from src.generated.instructions.multisig_add_member import (
    MultisigAddMemberAccounts,
    MultisigAddMemberArgs,
)
from src.generated.instructions.multisig_add_member import (
    multisig_add_member as multisig_add_member_instruction,
)
from src.generated.program_id import PROGRAM_ID
from src.generated.types.member import Member
from src.generated.types.multisig_add_member_args import (
    MultisigAddMemberArgs as MultisigAddMemberArgsType,
)


def multisig_add_member(
    multisig_pda: Pubkey,
    config_authority: Pubkey,
    rent_payer: Pubkey,
    new_member: Member,
    memo: str | None,
    program_id: Pubkey | None,
) -> Instruction:
    if program_id is None:
        program_id = PROGRAM_ID

    try:
        assert isinstance(multisig_pda, Pubkey)
        assert isinstance(config_authority, Pubkey)
        assert isinstance(rent_payer, Pubkey)
        assert isinstance(new_member, Member)
        assert isinstance(memo, str | None)
        assert isinstance(program_id, Pubkey)
    except AssertionError:
        raise ValueError("Invalid argument") from None

    accounts = MultisigAddMemberAccounts(
        multisig=multisig_pda,
        config_authority=config_authority,
        rent_payer=rent_payer,
    )
    args = MultisigAddMemberArgs(
        args=MultisigAddMemberArgsType(
            new_member=new_member,
            memo=memo,
        )
    )

    return multisig_add_member_instruction(
        accounts=accounts, args=args, program_id=program_id
    )
