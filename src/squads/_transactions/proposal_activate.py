from solders.hash import Hash
from solders.message import MessageV0
from solders.pubkey import Pubkey
from solders.transaction import Signer, VersionedTransaction

from ..instructions import proposal_activate as create_instruction


def proposal_activate(
    blockhash: Hash,
    fee_payer: Signer,
    multisig_pda: Pubkey,
    transaction_index: int,
    member: Signer,
    program_id: Pubkey | None,
) -> VersionedTransaction:
    """
    Returns `VersionedTransaction` that needs to be
    signed by `member` and `feePayer` before sending it.
    """
    try:
        assert isinstance(fee_payer, Signer)
        assert isinstance(multisig_pda, Pubkey)
        assert isinstance(transaction_index, int)
        assert isinstance(member, Signer)
        assert isinstance(program_id, Pubkey) or program_id is None
    except AssertionError:
        raise ValueError("Invalid argument") from None

    ix = create_instruction(
        multisig_pda,
        transaction_index,
        member.pubkey(),
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
