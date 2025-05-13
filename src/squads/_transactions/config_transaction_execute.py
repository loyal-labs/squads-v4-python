from collections.abc import Sequence

from solders.hash import Hash
from solders.message import MessageV0
from solders.pubkey import Pubkey
from solders.transaction import Signer, VersionedTransaction

from ..instructions import config_transaction_execute as create_instruction


def config_transaction_execute(
    blockhash: Hash,
    fee_payer: Signer,
    multisig_pda: Pubkey,
    transaction_index: int,
    member: Signer,
    rent_payer: Signer,
    spending_limits: list[Pubkey],
    program_id: Pubkey | None,
    signers: Sequence[Signer] | None = None,
) -> VersionedTransaction:
    """Execute a config transaction."""
    assert isinstance(blockhash, Hash)
    assert isinstance(fee_payer, Signer)
    assert isinstance(multisig_pda, Pubkey)
    assert isinstance(transaction_index, int)
    assert isinstance(member, Pubkey)
    assert isinstance(rent_payer, Pubkey)
    assert isinstance(spending_limits, list)
    assert isinstance(program_id, Pubkey) or program_id is None

    ix = create_instruction(
        multisig_pda,
        transaction_index,
        member,
        rent_payer,
        spending_limits,
        program_id,
    )
    message_v0 = MessageV0.try_compile(
        fee_payer.pubkey(),
        [ix],
        [],
        blockhash,
    )

    signers_array = [fee_payer, member, rent_payer]

    if signers is not None:
        signers_array.extend(signers)

    # only unique signers
    signers_array = list(set(signers_array))

    versioned_tx = VersionedTransaction(message_v0, signers_array)

    return versioned_tx
