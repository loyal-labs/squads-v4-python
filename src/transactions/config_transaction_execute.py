from solders.hash import Hash
from solders.message import MessageV0
from solders.pubkey import Pubkey
from solders.signature import Signature
from solders.transaction import VersionedTransaction

from src.instructions.config_transaction_execute import (
    config_transaction_execute as create_instruction,
)


def config_transaction_execute(
    blockhash: Hash,
    fee_payer: Pubkey,
    multisig_pda: Pubkey,
    transaction_index: int,
    member: Pubkey,
    rent_payer: Pubkey,
    spending_limits: list[Pubkey],
    program_id: Pubkey | None,
) -> VersionedTransaction:
    """
    Returns unsigned `VersionedTransaction` that needs to be
    signed by `configAuthority` and `feePayer` before sending it.
    """
    try:
        assert isinstance(blockhash, Hash)
        assert isinstance(fee_payer, Pubkey)
        assert isinstance(multisig_pda, Pubkey)
        assert isinstance(transaction_index, int)
        assert isinstance(member, Pubkey)
        assert isinstance(rent_payer, Pubkey)
        assert isinstance(spending_limits, list)
        assert isinstance(program_id, Pubkey) or program_id is None
    except AssertionError:
        raise ValueError("Invalid argument") from None

    ix = create_instruction(
        multisig_pda,
        transaction_index,
        member,
        rent_payer,
        spending_limits,
        program_id,
    )
    message_v0 = MessageV0.try_compile(
        fee_payer,
        [ix],
        [],
        blockhash,
    )
    num_signers = message_v0.header.num_required_signatures
    signers = [Signature.default() for _ in range(num_signers)]

    versioned_tx = VersionedTransaction.populate(message_v0, signers)

    return versioned_tx
