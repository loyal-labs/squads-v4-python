from solders.pubkey import Pubkey

from src.generated.instructions.proposal_approve import (
    ProposalApproveAccounts,
    ProposalApproveArgs,
)
from src.generated.instructions.proposal_approve import (
    proposal_approve as proposal_approve_instruction,
)
from src.generated.program_id import PROGRAM_ID
from src.generated.types.proposal_vote_args import ProposalVoteArgs
from src.pda import get_proposal_pda


def proposal_approve(
    multisig_pda: Pubkey,
    transaction_index: int,
    member: Pubkey,
    memo: str | None,
    program_id: Pubkey | None,
):
    if program_id is None:
        program_id = PROGRAM_ID

    proposal_pda = get_proposal_pda(multisig_pda, transaction_index, program_id)[0]

    accounts = ProposalApproveAccounts(
        multisig=multisig_pda,
        member=member,
        proposal=proposal_pda,
    )
    args = ProposalApproveArgs(
        args=ProposalVoteArgs(
            memo=memo,
        )
    )

    return proposal_approve_instruction(
        accounts=accounts, args=args, program_id=program_id
    )
