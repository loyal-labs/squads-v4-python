from collections.abc import Sequence

from solders.address_lookup_table_account import AddressLookupTableAccount
from solders.hash import Hash
from solders.instruction import CompiledInstruction, Instruction
from solders.message import MessageAddressTableLookup, MessageV0
from solders.pubkey import Pubkey

from utils.compiled_keys import CompiledKeys


def compile_to_wrapped_message_v0(
    payer_key: Pubkey,
    recent_blockhash: str,
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
    # These will store Pubkeys extracted into LUTs
    lut_writable_keys: Sequence[Pubkey] = []
    lut_readonly_keys: Sequence[Pubkey] = []

    active_address_lookup_table_accounts = address_lookup_table_accounts or []
    # Iterate over a copy of items if modifying the dict during iteration
    for lookup_table in active_address_lookup_table_accounts:
        extract_result = compiled_keys.extract_table_lookup(lookup_table)

        if extract_result is not None:
            # This should not happen if CompiledKeys.compile
            # correctly includes all keys
            address_table_lookup, extracted_keys_from_lut = extract_result
            address_table_lookups_list.extend([address_table_lookup])
            lut_writable_keys.extend(extracted_keys_from_lut.writable)
            lut_readonly_keys.extend(extracted_keys_from_lut.readonly)

    header, static_keys_list = compiled_keys.get_message_components()

    # The full list of accounts in the order they will appear in the message,
    # used for compiling instruction account indices.
    message_accounts_for_indexing: Sequence[Pubkey] = []

    # Order: static keys, then writable LUT keys, then readonly LUT keys.
    message_accounts_for_indexing.extend(static_keys_list)
    message_accounts_for_indexing.extend(lut_writable_keys)
    message_accounts_for_indexing.extend(lut_readonly_keys)

    compiled_instructions_list: Sequence[CompiledInstruction] = []

    for ix_input in instructions:
        try:
            program_id_index = message_accounts_for_indexing.index(ix_input.program_id)
        except ValueError:
            # This should not happen if CompiledKeys.compile
            # correctly includes all program_ids
            raise ValueError(
                f"Program ID {ix_input.program_id} not found in message accounts."
            ) from None

        account_indices: list[int] = []
        for acc_meta in ix_input.accounts:
            try:
                idx = message_accounts_for_indexing.index(acc_meta.pubkey)
                account_indices.append(idx)
            except ValueError:
                # This should not happen if CompiledKeys.compile
                # correctly includes all keys
                raise ValueError(
                    f"Account key {acc_meta.pubkey} from instruction "
                    f"{ix_input.program_id} not found in message accounts."
                ) from None

        compiled_instructions_list.append(
            CompiledInstruction(
                program_id_index=program_id_index,  # type: ignore # solders uses u8, direct int is fine
                accounts=bytes(account_indices),
                data=ix_input.data,
            )
        )

    recent_blockhash_hash_obj = Hash.from_string(recent_blockhash)

    # Construct MessageV0 directly using its components.
    # `static_keys_list` are the account keys not part of any lookup table.
    # `compiled_instructions_list` uses indices on `message_accounts_for_indexing`
    # `address_table_lookups_list` describes the LUTs used.
    return MessageV0(
        header=header,
        account_keys=static_keys_list,  # These are specifically the static keys
        recent_blockhash=recent_blockhash_hash_obj,
        instructions=compiled_instructions_list,
        address_table_lookups=address_table_lookups_list,
    )
