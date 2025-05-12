from collections.abc import Sequence

from solana.rpc.async_api import AsyncClient
from solders.address_lookup_table_account import AddressLookupTableAccount
from solders.hash import Hash
from solders.instruction import AccountMeta, Instruction
from solders.message import MessageAddressTableLookup, MessageV0
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
from src.pda import PDA
from src.types import TransactionMessageConstruct

from .compiled_keys import AccountKeysFromLookups, CompiledKeys, MessageAccountKeys


async def get_recent_blockhash(connection: AsyncClient) -> Hash:
    return (await connection.get_latest_blockhash()).value.blockhash


def compile_to_wrapped_message_v0(
    payer_key: Pubkey,
    recent_blockhash: Hash,
    instructions: Sequence[Instruction],
    address_lookup_table_accounts: Sequence[AddressLookupTableAccount] | None = None,
) -> MessageV0:
    """
    Compiles transaction components into a MessageV0 object, using a custom
    key compilation logic suitable for "wrapped" messages like Squads v4
    VaultTransaction.

    This function mirrors the behavior of a similar utility in the Squads v4
    TypeScript SDK, including the specific handling of program IDs and
    Address Lookup Tables (ALTs).

    Args:
        payer_key: The public key of the fee payer.
        recent_blockhash: The recent blockhash as a base58 encoded string.
        instructions: A sequence of transaction instructions to include.
                      Each instruction must conform to InputTransactionInstruction.
        address_lookup_table_accounts: An optional sequence of address lookup
                                       table accounts to use for compressing
                                       the message.

    Returns:
        A MessageV0 object ready for transaction signing and sending.
    """
    compiled_keys = CompiledKeys.compile(instructions, payer_key)

    address_table_lookups_list: Sequence[MessageAddressTableLookup] = []
    account_keys_from_lookups: AccountKeysFromLookups = AccountKeysFromLookups.empty()

    active_address_lookup_table_accounts = address_lookup_table_accounts or []
    # Iterate over a copy of items if modifying the dict during iteration
    for lookup_table in active_address_lookup_table_accounts:
        extract_result = compiled_keys.extract_table_lookup(lookup_table)

        if extract_result is not None:
            # This should not happen if CompiledKeys compile
            address_table_lookup, extracted_keys_from_lut = extract_result
            address_table_lookups_list.extend([address_table_lookup])
            account_keys_from_lookups.writable.extend(extracted_keys_from_lut.writable)
            account_keys_from_lookups.readonly.extend(extracted_keys_from_lut.readonly)

    header, static_account_keys = compiled_keys.get_message_components()

    account_keys = MessageAccountKeys(static_account_keys, account_keys_from_lookups)
    compiled_instructions = account_keys.compile_instructions(instructions)

    return MessageV0(
        header=header,
        account_keys=static_account_keys,
        recent_blockhash=recent_blockhash,
        instructions=compiled_instructions,
        address_table_lookups=address_table_lookups_list,
    )


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
) -> bytes:
    compiled_message = compile_to_wrapped_message_v0(
        payer_key=transaction_payer,
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

    for lut in compiled_message.address_table_lookups:
        lut_table_lookups.append(
            MultisigMessageAddressTableLookupJSON(
                account_key=str(lut.account_key),
                writable_indexes=list(lut.writable_indexes),
                readonly_indexes=list(lut.readonly_indexes),
            )
        )

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
    tx_msg_construct = TransactionMessageConstruct.from_json(construct_dict)
    tx_msg_bytes = tx_msg_construct.layout.build(tx_msg_construct.to_encodable())

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
        PDA.get_ephemeral_signer_pda(
            transaction_pda=transaction_pda,
            ephemeral_signer_index=additional_signer_index,
            program_id=program_id,
        )[0]
        for additional_signer_index, _ in enumerate(ephemeral_signer_bumps)
    ]

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
