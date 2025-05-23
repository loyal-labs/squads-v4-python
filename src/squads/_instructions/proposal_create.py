from solders.instruction import Instruction
from solders.pubkey import Pubkey

from .._internal.contants import MAX_SAFE_INTEGER
from ..accounts import PDA
from ..generated.instructions.proposal_create import (
    ProposalCreateAccounts,
    ProposalCreateArgs,
)
from ..generated.instructions.proposal_create import (
    proposal_create as proposal_create_instruction,
)
from ..generated.types.proposal_create_args import (
    ProposalCreateArgs as ProposalCreateArgsType,
)


def proposal_create(
    multisig_pda: Pubkey,
    creator: Pubkey,
    rent_payer: Pubkey | None,
    transaction_index: int,
    is_draft: bool,
    program_id: Pubkey,
) -> Instruction:
    assert isinstance(multisig_pda, Pubkey)
    assert isinstance(creator, Pubkey)
    assert isinstance(rent_payer, Pubkey) or rent_payer is None
    assert isinstance(transaction_index, int)
    assert isinstance(is_draft, bool)
    assert isinstance(program_id, Pubkey)

    proposal_pda = PDA.get_proposal_pda(multisig_pda, transaction_index, program_id)[0]

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
