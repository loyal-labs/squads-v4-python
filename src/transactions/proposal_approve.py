from solders.hash import Hash
from solders.message import MessageV0
from solders.pubkey import Pubkey
from solders.signature import Signature
from solders.transaction import VersionedTransaction

from src.instructions.proposal_approve import proposal_approve as create_instruction


def proposal_approve(
    blockhash: Hash,
    fee_payer: Pubkey,
    multisig_pda: Pubkey,
    transaction_index: int,
    member: Pubkey,
    memo: str | None,
    program_id: Pubkey | None,
) -> VersionedTransaction:
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
