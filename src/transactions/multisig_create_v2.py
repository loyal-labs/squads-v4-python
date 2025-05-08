from solders.hash import Hash
from solders.message import Message
from solders.pubkey import Pubkey
from solders.transaction import Transaction

from src.generated.types.member import Member
from src.instructions.multisig_create_v2 import multisig_create_v2 as create_instruction


def multisig_create_v2(
    blockhash: Hash,
    treasury: Pubkey,
    create_key: Pubkey,
    creator: Pubkey,
    multisig: Pubkey,
    config_authority: Pubkey | None,
    threshold: int,
    members: list[Member],
    time_lock: int,
    rent_collector: Pubkey | None,
    memo: str | None,
    program_id: Pubkey,
) -> Transaction:
    """
    Returns unsigned `Transaction` that needs to be
    signed by `creator` and `createKey` before sending it.
    """
    instruction = create_instruction(
        treasury,
        creator,
        multisig,
        config_authority,
        threshold,
        members,
        time_lock,
        create_key,
        rent_collector,
        memo,
        program_id,
    )

    message = Message(instructions=[instruction], payer=creator)

    return Transaction.new_unsigned(message)
