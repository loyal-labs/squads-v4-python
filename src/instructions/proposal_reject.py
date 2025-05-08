from solders.instruction import Instruction
from solders.pubkey import Pubkey

from src.generated.instructions.proposal_reject import (
    ProposalRejectAccounts,
    ProposalRejectArgs,
)
from src.generated.instructions.proposal_reject import (
    proposal_reject as proposal_reject_instruction,
)
from src.generated.program_id import PROGRAM_ID
from src.generated.types.proposal_vote_args import ProposalVoteArgs
from src.pda import get_proposal_pda


def proposal_reject(
    multisig_pda: Pubkey,
    transaction_index: int,
    member: Pubkey,
    memo: str | None,
    program_id: Pubkey | None,
) -> Instruction:
    if program_id is None:
        program_id = PROGRAM_ID

    try:
        assert isinstance(multisig_pda, Pubkey)
        assert isinstance(transaction_index, int)
        assert isinstance(member, Pubkey)
        assert isinstance(memo, str) or memo is None
        assert isinstance(program_id, Pubkey)
    except AssertionError:
        raise ValueError("Invalid argument") from None

    proposal_pda = get_proposal_pda(multisig_pda, transaction_index, program_id)[0]

    accounts = ProposalRejectAccounts(
        multisig=multisig_pda,
        member=member,
        proposal=proposal_pda,
    )
    args = ProposalRejectArgs(
        args=ProposalVoteArgs(
            memo=memo,
        )
    )

    return proposal_reject_instruction(
        accounts=accounts, args=args, program_id=program_id
    )
