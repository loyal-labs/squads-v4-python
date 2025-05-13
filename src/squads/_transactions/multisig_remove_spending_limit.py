from collections.abc import Sequence

from solders.hash import Hash
from solders.message import MessageV0
from solders.pubkey import Pubkey
from solders.transaction import Signer, VersionedTransaction

from ..instructions import multisig_remove_spending_limit as create_instruction


def multisig_remove_spending_limit(
    blockhash: Hash,
    fee_payer: Signer,
    multisig_pda: Pubkey,
    config_authority: Pubkey,
    spending_limit: Pubkey,
    rent_collector: Pubkey,
    memo: str | None,
    program_id: Pubkey | None,
    signers: Sequence[Signer] | None,
) -> VersionedTransaction:
    """
    Returns unsigned `VersionedTransaction` that needs to be
    signed by `configAuthority` and `feePayer` before sending it.
    """
    assert isinstance(blockhash, Hash)
    assert isinstance(fee_payer, Signer)
    assert isinstance(multisig_pda, Pubkey)
    assert isinstance(config_authority, Pubkey)
    assert isinstance(spending_limit, Pubkey)
    assert isinstance(rent_collector, Pubkey)
    assert isinstance(memo, str) or memo is None
    assert isinstance(program_id, Pubkey) or program_id is None
    assert isinstance(signers, Sequence) or signers is None

    ix = create_instruction(
        multisig_pda,
        config_authority,
        spending_limit,
        rent_collector,
        memo,
        program_id,
    )
    message_v0 = MessageV0.try_compile(
        fee_payer.pubkey(),
        [ix],
        [],
        blockhash,
    )
    signers_list = [fee_payer]
    if signers is not None:
        signers_list.extend(signers)

    # only unique signers
    signers_list = list(set(signers_list))

    versioned_tx = VersionedTransaction(message_v0, signers_list)

    return versioned_tx
