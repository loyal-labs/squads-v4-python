from solders.instruction import Instruction
from solders.pubkey import Pubkey

from ..accounts import PDA
from ..generated.instructions.proposal_cancel_v2 import (
    ProposalCancelV2Accounts,
    ProposalCancelV2Args,
    ProposalVoteNested,
)
from ..generated.instructions.proposal_cancel_v2 import (
    proposal_cancel_v2 as proposal_cancel_v2_instruction,
)
from ..generated.program_id import PROGRAM_ID
from ..generated.types.proposal_vote_args import ProposalVoteArgs


def proposal_cancel_v2(
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

    proposal_pda = PDA.get_proposal_pda(multisig_pda, transaction_index, program_id)[0]

    accounts = ProposalCancelV2Accounts(
        proposal_vote=ProposalVoteNested(
            multisig=multisig_pda,
            member=member,
            proposal=proposal_pda,
        )
    )

    args = ProposalCancelV2Args(
        args=ProposalVoteArgs(
            memo=memo,
        )
    )

    return proposal_cancel_v2_instruction(
        accounts=accounts, args=args, program_id=program_id
    )
