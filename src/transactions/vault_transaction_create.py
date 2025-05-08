from solders.address_lookup_table_account import AddressLookupTableAccount
from solders.hash import Hash
from solders.message import Message, MessageV0
from solders.pubkey import Pubkey
from solders.signature import Signature
from solders.transaction import VersionedTransaction

from src.instructions.vault_transaction_create import (
    vault_transaction_create as create_instruction,
)


def vault_transaction_create(
    blockhash: Hash,
    fee_payer: Pubkey,
    multisig_pda: Pubkey,
    transaction_index: int,
    creator: Pubkey,
    rent_payer: Pubkey,
    vault_index: int,
    ephemeral_signers: int,
    transaction_message: Message,
    address_lookup_table_accounts: list[AddressLookupTableAccount],
    memo: str | None,
    program_id: Pubkey | None,
) -> VersionedTransaction:
    """
    Returns unsigned `VersionedTransaction` that needs to be
    signed by `creator` and `createKey` before sending it.
    """
    try:
        assert isinstance(fee_payer, Pubkey)
        assert isinstance(multisig_pda, Pubkey)
        assert isinstance(transaction_index, int)
        assert isinstance(creator, Pubkey)
        assert isinstance(rent_payer, Pubkey)
        assert isinstance(vault_index, int)
        assert isinstance(ephemeral_signers, int)
        assert isinstance(transaction_message, Message)
        assert isinstance(address_lookup_table_accounts, list)
        assert isinstance(memo, str) or memo is None
        assert isinstance(program_id, Pubkey) or program_id is None
    except AssertionError:
        raise ValueError("Invalid argument") from None

    ix = create_instruction(
        multisig_pda,
        transaction_index,
        creator,
        rent_payer,
        vault_index,
        ephemeral_signers,
        transaction_message,
        address_lookup_table_accounts,
        memo,
        program_id,
    )

    message_v0 = MessageV0.try_compile(
        creator,
        [ix],
        [],
        blockhash,
    )
    num_signers = message_v0.header.num_required_signatures
    signers = [Signature.default() for _ in range(num_signers)]

    versioned_tx = VersionedTransaction.populate(message_v0, signers)

    return versioned_tx
