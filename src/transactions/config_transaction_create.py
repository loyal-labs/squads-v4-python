from solders.hash import Hash
from solders.message import MessageV0
from solders.pubkey import Pubkey
from solders.signature import Signature
from solders.transaction import Signer, VersionedTransaction

from src.generated.types.config_action import ConfigActionKind
from src.instructions.config_transaction_create import (
    config_transaction_create as create_instruction,
)


def config_transaction_create(
    blockhash: Hash,
    fee_payer: Signer,
    multisig_pda: Pubkey,
    transaction_index: int,
    creator: Signer,
    rent_payer: Pubkey,
    actions: list[ConfigActionKind],
    memo: str | None,
    program_id: Pubkey | None,
) -> VersionedTransaction:
    """
    Returns `VersionedTransaction` that needs to be
    signed by `configAuthority` and `feePayer` before sending it.
    """
    assert isinstance(blockhash, Hash)
    assert isinstance(fee_payer, Signer)
    assert isinstance(multisig_pda, Pubkey)
    assert isinstance(transaction_index, int)
    assert isinstance(creator, Signer)
    assert isinstance(rent_payer, Pubkey)
    assert isinstance(actions, list)
    assert isinstance(memo, str) or memo is None
    assert isinstance(program_id, Pubkey) or program_id is None

    ix = create_instruction(
        multisig_pda,
        transaction_index,
        creator.pubkey(),
        rent_payer,
        actions,
        memo,
        program_id,
    )
    try:
        message_v0 = MessageV0.try_compile(
            fee_payer.pubkey(),
            [ix],
            [],
            blockhash,
        )
    except Exception as e:
        raise e from None

    versioned_tx = VersionedTransaction(message_v0, [fee_payer])

    return versioned_tx
