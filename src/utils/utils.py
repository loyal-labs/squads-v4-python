from collections.abc import Sequence
from typing import Any

from borsh_construct import U8
from construct import Array, Construct
from solana.rpc.async_api import AsyncClient
from solders.address_lookup_table_account import AddressLookupTableAccount
from solders.instruction import AccountMeta
from solders.message import Message
from solders.pubkey import Pubkey

from src.generated.types.vault_transaction_message import VaultTransactionMessage
from src.pda import get_ephemeral_signer_pda
from src.types import TransactionMessage
from src.utils.compile_to_wrapped_message_v0 import compile_to_wrapped_message_v0

MAX_TX_SIZE_BYTES = 1232
STRING_LEN_SIZE = 4


def create_small_array(  # type: ignore
    length: int,
    construct: Construct = U8,  # type: ignore
) -> Array:  # type: ignore
    """
    Creates a small array of the given length.
    """
    try:
        assert length > 0
        assert length <= 32
    except AssertionError:
        raise ValueError("Length must be between 1 and 32") from None

    return construct[length]  # type: ignore


def get_available_memo_size(tx_without_memo: bytes) -> int:
    tx_size = len(tx_without_memo)
    # Sometimes long memo can trigger switching
    # from 1 to 2 bytes length encoding in Compact-u16,
    # so we reserve 1 extra byte to make sure.
    return MAX_TX_SIZE_BYTES - tx_size - STRING_LEN_SIZE - 1


def is_static_writable_index(
    message: VaultTransactionMessage,
    index: int,
) -> bool:
    num_acc_keys = len(message.account_keys)
    num_signers = message.num_signers
    num_writable_signers = message.num_writable_signers
    num_writable_non_signers = message.num_writable_non_signers

    if index >= num_acc_keys:
        # `index` is not a part of static `account_keys`.
        return False

    if index < num_writable_signers:
        # `index` is within the range of writable signer keys.
        return True

    if index >= num_signers:
        # `index` is within the range of non-signer keys.
        index_into_non_signers = index - num_signers
        # Whether `index` is within the range of writable non-signer keys.
        return index_into_non_signers < num_writable_non_signers

    return False


def is_signer_index(message: VaultTransactionMessage, index: int) -> bool:
    return index < message.num_signers


def transaction_message_to_multisig_transaction_message_bytes(
    message: Message,
    address_lookup_table_accounts: list[AddressLookupTableAccount] | None,
    vault_pda: Pubkey,
) -> bytes:
    # Use custom implementation of `message.compileToV0Message`
    # that allows instruction programIds
    # to also be loaded from `addressLookupTableAccounts`.
    payer_key = message.account_keys[0]
    recent_blockhash = message.recent_blockhash
    instructions = message.instructions

    compiled_message = compile_to_wrapped_message_v0(
        payer_key=payer_key,
        recent_blockhash=recent_blockhash,
        instructions=instructions,
        address_lookup_table_accounts=address_lookup_table_accounts,
    )

    compiled_instructions = [
        {
            "program_id_index": ix.program_id_index,
            "account_indexes": ix.accounts,
            "data": ix.data,
        }
        for ix in compiled_message.instructions
    ]

    transaction_message_construct = TransactionMessage.construct()  # type: ignore

    construct_dict = {
        "num_signers": compiled_message.header.num_required_signatures,
        "num_writable_signers": compiled_message.header.num_required_signatures
        - compiled_message.header.num_readonly_signed_accounts,
        "num_writable_non_signers": len(compiled_message.account_keys)
        - compiled_message.header.num_required_signatures
        - compiled_message.header.num_readonly_unsigned_accounts,
        "account_keys": compiled_message.account_keys,
        "instructions": compiled_instructions,
        "address_table_lookups": compiled_message.address_table_lookups,
    }

    transaction_message_bytes = transaction_message_construct.build(construct_dict)  # type: ignore
    return transaction_message_bytes


async def accounts_for_transaction_execute(
    connection: AsyncClient,
    transaction_pda: Pubkey,
    vault_pda: Pubkey,
    message: VaultTransactionMessage,
    ephemeral_signer_bump: Sequence[int],
    program_id: Pubkey | None,
) -> dict[str, Any]:
    ephemeral_signer_pdas: Sequence[Pubkey] = [
        get_ephemeral_signer_pda(transaction_pda, ix, program_id)[0]
        for ix in ephemeral_signer_bump
    ]

    address_lookup_table_keys = [
        lookup.account_key for lookup in message.address_table_lookups
    ]
    address_lookup_dict: dict[Pubkey, AddressLookupTableAccount] = {}

    # Initialize RPC client
    # TODO: double check if this is correct
    async with connection as client:
        # Create tasks for fetching all tables
        lookup_tasks: list[tuple[Pubkey, AddressLookupTableAccount]] = []

        # TODO: do it in concurrently
        for key in address_lookup_table_keys:
            response = await client.get_account_info(key, encoding="jsonParsed")
            account_info = response.value
            if account_info is None:
                raise ValueError("Address lookup table account %s not found", key)

            value_obj = AddressLookupTableAccount.from_bytes(account_info.data)

            result = (key, value_obj)
            lookup_tasks.extend([result])

        address_lookup_dict = dict(lookup_tasks)

    # Populate account metas required for execution of the transaction.
    account_metas: Sequence[AccountMeta] = []

    # First add the lookup table accounts used by the transaction.
    # They are needed for on-chain validation.
    account_metas.extend(
        [AccountMeta(key, False, False) for key in address_lookup_dict.keys()]
    )

    # Then add static account keys included into the message.
    for index, key in enumerate(message.account_keys):
        pubkey = key
        is_writable = is_static_writable_index(message, index)
        # NOTE: vaultPda and ephemeralSignerPdas cannot be marked as signers,
        # because they are PDAs and won't have
        # their signatures on the transaction.
        is_signer = (
            is_signer_index(message, index)
            and not key == vault_pda
            and not any(key == k for k in ephemeral_signer_pdas)
        )

        meta = AccountMeta(pubkey, is_writable, is_signer)
        account_metas.extend([meta])

    # Then add accounts that will be loaded with address lookup tables.
    for lookup in message.address_table_lookups:
        pubkey = lookup.account_key
        lookup_account = address_lookup_dict[pubkey]

        assert lookup_account, (
            "Address lookup table account %s not found",
            pubkey,
        )

        for idx in lookup.writable_indexes:
            pubkey = lookup_account.addresses[idx]

            assert pubkey, (
                "Address lookup table account %s has no owner",
                lookup_account.key,
            )

            meta = AccountMeta(pubkey, True, False)
            account_metas.extend([meta])

        for idx in lookup.readonly_indexes:
            pubkey = lookup_account.addresses[idx]
            assert pubkey, (
                "Address lookup table account %s has no owner",
                lookup_account.key,
            )

            meta = AccountMeta(pubkey, False, False)
            account_metas.extend([meta])

    return {
        "account_metas": account_metas,
        "lookup_table_accounts": list(address_lookup_dict.values()),
    }
