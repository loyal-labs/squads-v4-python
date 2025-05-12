from solders.address_lookup_table_account import AddressLookupTableAccount
from solders.hash import Hash
from solders.instruction import Instruction
from solders.message import MessageV0
from solders.pubkey import Pubkey
from solders.transaction import Signer, VersionedTransaction

from src.instructions.vault_transaction_create import (
    vault_transaction_create as create_instruction,
)


def vault_transaction_create(
    blockhash: Hash,
    fee_payer: Signer,
    multisig_pda: Pubkey,
    transaction_index: int,
    creator: Signer,
    rent_payer: Signer | None,
    vault_index: int,
    ephemeral_signers: int,
    transaction_payer: Pubkey,
    transaction_recent_blockhash: Hash,
    transaction_instructions: list[Instruction],
    address_lookup_table_accounts: list[AddressLookupTableAccount] | None,
    memo: str | None,
    program_id: Pubkey,
    signers: list[Signer] | None,
) -> VersionedTransaction:
    """
    Returns `VersionedTransaction` that needs to be
    signed by `creator` and `createKey` before sending it.
    """
    assert isinstance(fee_payer, Signer)
    assert isinstance(multisig_pda, Pubkey)
    assert isinstance(transaction_index, int)
    assert isinstance(creator, Signer)
    assert isinstance(rent_payer, Signer) or rent_payer is None
    assert isinstance(vault_index, int)
    assert isinstance(ephemeral_signers, int)
    assert isinstance(transaction_payer, Pubkey)
    assert isinstance(transaction_recent_blockhash, Hash)
    assert isinstance(transaction_instructions, list)
    assert (
        isinstance(address_lookup_table_accounts, list)
        or address_lookup_table_accounts is None
    )
    assert isinstance(memo, str) or memo is None
    assert isinstance(program_id, Pubkey) or program_id is None
    assert isinstance(signers, list) or signers is None

    ix = create_instruction(
        multisig_pda,
        transaction_index,
        creator.pubkey(),
        rent_payer.pubkey() if rent_payer else None,
        vault_index,
        ephemeral_signers,
        transaction_payer,
        transaction_recent_blockhash,
        transaction_instructions,
        address_lookup_table_accounts,
        memo,
        program_id,
    )

    message_v0 = MessageV0.try_compile(
        creator.pubkey(),
        [ix],
        [],
        blockhash,
    )

    signers_list = [fee_payer]
    if signers:
        signers_list.extend(signers)

    versioned_tx = VersionedTransaction(message_v0, signers_list)

    return versioned_tx
