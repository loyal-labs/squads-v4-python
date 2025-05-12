from solders.hash import Hash
from solders.message import MessageV0
from solders.pubkey import Pubkey
from solders.transaction import Signer, VersionedTransaction

from src.instructions.proposal_reject import proposal_reject as create_instruction


def proposal_reject(
    blockhash: Hash,
    fee_payer: Signer,
    multisig_pda: Pubkey,
    transaction_index: int,
    member: Signer,
    memo: str | None,
    program_id: Pubkey,
) -> VersionedTransaction:
    """
    Returns `VersionedTransaction` that needs to be
    signed by `member` and `feePayer` before sending it.
    """
    assert isinstance(fee_payer, Signer)
    assert isinstance(multisig_pda, Pubkey)
    assert isinstance(transaction_index, int)
    assert isinstance(member, Signer)
    assert isinstance(memo, str) or memo is None
    assert isinstance(program_id, Pubkey)

    ix = create_instruction(
        multisig_pda,
        transaction_index,
        member.pubkey(),
        memo,
        program_id,
    )
    message_v0 = MessageV0.try_compile(
        fee_payer.pubkey(),
        [ix],
        [],
        blockhash,
    )
    signers_list = [fee_payer, member]

    # unique signers
    signers_list = list(set(signers_list))

    versioned_tx = VersionedTransaction(message_v0, signers_list)

    return versioned_tx
