from solders.instruction import Instruction
from solders.pubkey import Pubkey

from src.generated.instructions.proposal_activate import ProposalActivateAccounts
from src.generated.instructions.proposal_activate import (
    proposal_activate as proposal_activate_instruction,
)
from src.generated.program_id import PROGRAM_ID
from src.pda import get_proposal_pda


def proposal_activate(
    multisig_pda: Pubkey,
    transaction_index: int,
    member: Pubkey,
    program_id: Pubkey | None,
) -> Instruction:
    if program_id is None:
        program_id = PROGRAM_ID

    try:
        assert isinstance(multisig_pda, Pubkey)
        assert isinstance(transaction_index, int)
        assert isinstance(member, Pubkey)
        assert isinstance(program_id, Pubkey)
    except AssertionError:
        raise ValueError("Invalid argument") from None

    proposal_pda = get_proposal_pda(multisig_pda, transaction_index, program_id)[0]

    accounts = ProposalActivateAccounts(
        multisig=multisig_pda,
        proposal=proposal_pda,
        member=member,
    )

    return proposal_activate_instruction(accounts=accounts, program_id=program_id)
