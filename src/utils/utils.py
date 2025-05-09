from collections.abc import Sequence

from borsh_construct import U8
from construct import Array, Construct
from solana.rpc.async_api import AsyncClient
from solders.address_lookup_table_account import AddressLookupTableAccount
from solders.hash import Hash
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from src.generated.types.multisig_compiled_instruction import (
    MultisigCompiledInstructionJSON,
)
from src.generated.types.multisig_message_address_table_lookup import (
    MultisigMessageAddressTableLookupJSON,
)
from src.generated.types.vault_transaction_message import (
    VaultTransactionMessage,
    VaultTransactionMessageJSON,
)
from src.pda import get_ephemeral_signer_pda
from src.utils.compile_to_wrapped_message_v0 import compile_to_wrapped_message_v0
from src.utils.compiled_keys import CompiledKeys

MAX_TX_SIZE_BYTES = 1232
STRING_LEN_SIZE = 4


def create_small_array(  # type: ignore
    length: Construct,  # type: ignore
    construct: Construct = U8,  # type: ignore
) -> Array:  # type: ignore
    """
    Creates a small array of the given length.
    """
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
    transaction_payer: Pubkey,
    transaction_recent_blockhash: Hash,
    transaction_instructions: list[Instruction],
    address_lookup_table_accounts: list[AddressLookupTableAccount],
    vault_pda: Pubkey,
) -> bytes:
    compiled_keys = CompiledKeys.compile(transaction_instructions, transaction_payer)

    compiled_message = compile_to_wrapped_message_v0(
        compiled_keys=compiled_keys,
        recent_blockhash=transaction_recent_blockhash,
        instructions=transaction_instructions,
        address_lookup_table_accounts=address_lookup_table_accounts,
    )

    compiled_instructions = [
        MultisigCompiledInstructionJSON(
            program_id_index=ix.program_id_index,
            account_indexes=list(ix.accounts),
            data=list(ix.data),
        )
        for ix in compiled_message.instructions
    ]

    lut_table_lookups: list[MultisigMessageAddressTableLookupJSON] = []
    for lut_account in address_lookup_table_accounts:
        table = compiled_keys.extract_table_lookup(lut_account)
        if table is None:
            continue
        msg_lut_table, _ = table
        lut_obj = MultisigMessageAddressTableLookupJSON(
            account_key=str(msg_lut_table.account_key),
            writable_indexes=list(msg_lut_table.writable_indexes),
            readonly_indexes=list(msg_lut_table.readonly_indexes),
        )
        lut_table_lookups.extend([lut_obj])

    acc_keys = [str(key) for key in compiled_message.account_keys]
    construct_dict = VaultTransactionMessageJSON(
        num_signers=compiled_message.header.num_required_signatures,
        num_writable_signers=compiled_message.header.num_required_signatures
        - compiled_message.header.num_readonly_signed_accounts,
        num_writable_non_signers=len(compiled_message.account_keys)
        - compiled_message.header.num_required_signatures
        - compiled_message.header.num_readonly_unsigned_accounts,
        account_keys=acc_keys,
        instructions=compiled_instructions,
        address_table_lookups=lut_table_lookups,
    )

    tx_msg_obj = VaultTransactionMessage.from_json(construct_dict)
    tx_msg_bytes = tx_msg_obj.layout.build(tx_msg_obj.to_encodable())

    return tx_msg_bytes


async def _create_address_lookup_table_accounts(
    connection: AsyncClient, address_lookup_table_keys: list[Pubkey]
) -> dict[Pubkey, AddressLookupTableAccount]:
    # Initialize an empty dictionary
    lookup_tasks: list[tuple[Pubkey, AddressLookupTableAccount]] = []

    # Process each key sequentially
    for key in address_lookup_table_keys:
        # Fetch the lookup table
        response = await connection.get_account_info(key, encoding="jsonParsed")
        value = response.value

        # Check if the value exists
        if not value:
            raise ValueError(f"Address lookup table account {key} not found")

        # Add to the dictionary
        value_obj = AddressLookupTableAccount.from_bytes(value.data)
        lookup_tasks.extend([(key, value_obj)])

    print(f"Lookup tasks: {len(lookup_tasks)}")

    return dict(lookup_tasks)


async def accounts_for_transaction_execute(
    connection: AsyncClient,
    transaction_pda: Pubkey,
    vault_pda: Pubkey,
    message: VaultTransactionMessage,
    ephemeral_signer_bumps: Sequence[int],
    program_id: Pubkey | None,
) -> tuple[list[AccountMeta], list[AddressLookupTableAccount]]:
    print(f"Ephemeral signer bumps: {ephemeral_signer_bumps}")
    ephemeral_signer_pdas = [
        get_ephemeral_signer_pda(
            transaction_pda=transaction_pda,
            ephemeral_signer_index=additional_signer_index,
            program_id=program_id,
        )[0]
        for additional_signer_index, _ in enumerate(ephemeral_signer_bumps)
    ]
    print(f"Ephemeral signer pdas: {ephemeral_signer_pdas}")

    address_lookup_table_keys = [
        lookup.account_key for lookup in message.address_table_lookups
    ]
    address_lookup_dict = await _create_address_lookup_table_accounts(
        connection, address_lookup_table_keys
    )

    # Populate account metas required for execution of the transaction.
    account_metas: list[AccountMeta] = []

    # First add the lookup table accounts used by the transaction.
    # They are needed for on-chain validation.
    account_metas.extend(
        [AccountMeta(key, False, False) for key in address_lookup_dict.keys()]
    )

    # Then add static account keys included into the message.
    for index, key in enumerate(message.account_keys):
        is_ephemeral_signer = any(key == k for k in ephemeral_signer_pdas)

        pubkey = key
        # vaultPda and ephemeralSignerPdas cannot be marked as signers,
        # they are PDAs and won't have their signatures on the transaction.
        is_writable = is_static_writable_index(message, index)
        print(f"Key: {key}, is ephemeral signer: {is_ephemeral_signer}")

        meta = AccountMeta(
            pubkey,
            is_writable=is_writable,
            is_signer=(
                is_signer_index(message, index)
                and key != vault_pda
                and not is_ephemeral_signer
            ),
        )
        account_metas.append(meta)

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

    return account_metas, list(address_lookup_dict.values())
