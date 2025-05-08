from solders.message import Message
from solders.pubkey import Pubkey
from solders.transaction import Transaction

from src.instructions.proposal_approve import proposal_approve as create_instruction


def proposal_approve(
    fee_payer: Pubkey,
    multisig_pda: Pubkey,
    transaction_index: int,
    member: Pubkey,
    memo: str | None,
    program_id: Pubkey | None,
) -> Transaction:
    """
    Returns unsigned `Transaction` that needs to be
    signed by `member` and `feePayer` before sending it.
    """
    try:
        assert isinstance(fee_payer, Pubkey)
        assert isinstance(multisig_pda, Pubkey)
        assert isinstance(transaction_index, int)
        assert isinstance(member, Pubkey)
        assert isinstance(memo, str) or memo is None
        assert isinstance(program_id, Pubkey) or program_id is None
    except AssertionError:
        raise ValueError("Invalid argument") from None

    ix = create_instruction(
        multisig_pda,
        transaction_index,
        member,
        memo,
        program_id,
    )

    message = Message(instructions=[ix], payer=fee_payer)

    return Transaction.new_unsigned(message)
