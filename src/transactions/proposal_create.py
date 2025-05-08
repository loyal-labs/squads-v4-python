from solders.message import Message
from solders.pubkey import Pubkey
from solders.transaction import Transaction

from src.instructions.proposal_create import proposal_create as create_instruction


def proposal_create(
    fee_payer: Pubkey,
    multisig_pda: Pubkey,
    transaction_index: int,
    creator: Pubkey,
    rent_payer: Pubkey | None,
    is_draft: bool | None,
    program_id: Pubkey | None,
) -> Transaction:
    """
    Returns unsigned `Transaction` that needs to be
    signed by `creator` and `createKey` before sending it.
    """
    try:
        assert isinstance(fee_payer, Pubkey)
        assert isinstance(multisig_pda, Pubkey)
        assert isinstance(transaction_index, int)
        assert isinstance(creator, Pubkey)
        assert isinstance(rent_payer, Pubkey) or rent_payer is None
        assert isinstance(is_draft, bool) or is_draft is None
        assert isinstance(program_id, Pubkey) or program_id is None
    except AssertionError:
        raise ValueError("Invalid argument") from None

    ix = create_instruction(
        multisig_pda,
        creator,
        rent_payer,
        transaction_index,
        is_draft,
        program_id,
    )

    message = Message(instructions=[ix], payer=creator)

    return Transaction.new_unsigned(message)
