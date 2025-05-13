from collections.abc import Sequence

from solders.hash import Hash
from solders.message import MessageV0
from solders.pubkey import Pubkey
from solders.transaction import Signer, VersionedTransaction

from ..generated.types.config_action import ConfigActionKind
from ..instructions import config_transaction_create as create_instruction


def config_transaction_create(
    blockhash: Hash,
    fee_payer: Signer,
    multisig_pda: Pubkey,
    transaction_index: int,
    creator: Pubkey,
    rent_payer: Pubkey,
    actions: list[ConfigActionKind],
    memo: str | None,
    program_id: Pubkey,
    signers: Sequence[Signer] | None = None,
) -> VersionedTransaction:
    assert isinstance(blockhash, Hash)
    assert isinstance(fee_payer, Signer)
    assert isinstance(multisig_pda, Pubkey)
    assert isinstance(transaction_index, int)
    assert isinstance(creator, Pubkey)
    assert isinstance(rent_payer, Pubkey)
    assert isinstance(actions, list)
    assert isinstance(memo, str) or memo is None
    assert isinstance(program_id, Pubkey)

    ix = create_instruction(
        multisig_pda,
        transaction_index,
        creator,
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

    signers_array = [fee_payer]
    if signers is not None:
        signers_array.extend(signers)

    # only unique signers
    signers_array = list(set(signers_array))

    versioned_tx = VersionedTransaction(message_v0, signers_array)

    return versioned_tx
