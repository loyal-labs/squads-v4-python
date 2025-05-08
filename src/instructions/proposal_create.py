from solders.instruction import Instruction
from solders.pubkey import Pubkey

from src.generated.instructions.proposal_create import (
    ProposalCreateAccounts,
    ProposalCreateArgs,
)
from src.generated.instructions.proposal_create import (
    proposal_create as proposal_create_instruction,
)
from src.generated.program_id import PROGRAM_ID
from src.generated.types.proposal_create_args import (
    ProposalCreateArgs as ProposalCreateArgsType,
)
from src.pda import get_proposal_pda
from src.utils.contants import MAX_SAFE_INTEGER


def proposal_create(
    multisig_pda: Pubkey,
    creator: Pubkey,
    rent_payer: Pubkey | None,
    transaction_index: int,
    is_draft: bool | None,
    program_id: Pubkey | None,
) -> Instruction:
    if program_id is None:
        program_id = PROGRAM_ID

    if is_draft is None:
        is_draft = False

    try:
        assert isinstance(multisig_pda, Pubkey)
        assert isinstance(creator, Pubkey)
        assert isinstance(rent_payer, Pubkey) or rent_payer is None
        assert isinstance(transaction_index, int)
        assert isinstance(is_draft, bool) or is_draft is None
        assert isinstance(program_id, Pubkey)
    except AssertionError:
        raise ValueError("Invalid argument") from None

    proposal_pda = get_proposal_pda(multisig_pda, transaction_index, program_id)[0]

    if transaction_index > MAX_SAFE_INTEGER:
        raise ValueError("transaction_index is too large")

    accounts = ProposalCreateAccounts(
        creator=creator,
        rent_payer=rent_payer if rent_payer is not None else creator,
        multisig=multisig_pda,
        proposal=proposal_pda,
    )
    args = ProposalCreateArgs(
        args=ProposalCreateArgsType(transaction_index=transaction_index, draft=is_draft)
    )

    return proposal_create_instruction(
        accounts=accounts, args=args, program_id=program_id
    )
