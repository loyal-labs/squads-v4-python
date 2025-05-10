from collections.abc import Sequence

from solders.address_lookup_table_account import AddressLookupTableAccount
from solders.hash import Hash
from solders.instruction import Instruction
from solders.message import MessageAddressTableLookup, MessageV0
from solders.pubkey import Pubkey

from src.utils.compiled_keys import (
    AccountKeysFromLookups,
    CompiledKeys,
    MessageAccountKeys,
)


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
