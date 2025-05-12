from solders.hash import Hash
from solders.message import MessageV0
from solders.pubkey import Pubkey
from solders.transaction import Signer, VersionedTransaction

from src.instructions.proposal_create import proposal_create as create_instruction


def proposal_create(
    blockhash: Hash,
    fee_payer: Signer,
    multisig_pda: Pubkey,
    transaction_index: int,
    creator: Signer,
    rent_payer: Signer | None,
    is_draft: bool,
    program_id: Pubkey,
) -> VersionedTransaction:
    assert isinstance(fee_payer, Signer)
    assert isinstance(multisig_pda, Pubkey)
    assert isinstance(transaction_index, int)
    assert isinstance(creator, Signer)
    assert isinstance(rent_payer, Signer) or rent_payer is None
    assert isinstance(is_draft, bool)
    assert isinstance(program_id, Pubkey)

    ix = create_instruction(
        multisig_pda,
        creator.pubkey(),
        rent_payer.pubkey() if rent_payer else None,
        transaction_index,
        is_draft,
        program_id,
    )

    message_v0 = MessageV0.try_compile(
        creator.pubkey(),
        [ix],
        [],
        blockhash,
    )
    signers_list = (
        [fee_payer, creator, rent_payer] if rent_payer else [fee_payer, creator]
    )

    # unique signers
    signers_list = list(set(signers_list))

    versioned_tx = VersionedTransaction(message_v0, signers_list)

    return versioned_tx
