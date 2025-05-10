from collections.abc import Callable, Sequence
from dataclasses import dataclass

from pydantic import BaseModel
from solders.address_lookup_table_account import AddressLookupTableAccount
from solders.instruction import CompiledInstruction, Instruction
from solders.message import MessageAddressTableLookup, MessageHeader
from solders.pubkey import Pubkey

from src.utils.contants import U8_MAX


@dataclass
class AccountKeysFromLookups:
    writable: list[Pubkey]
    readonly: list[Pubkey]

    @classmethod
    def empty(cls) -> "AccountKeysFromLookups":
        return cls(writable=[], readonly=[])


class MessageAccountKeys:
    def __init__(
        self,
        static_account_keys: Sequence[Pubkey],
        account_keys_from_lookups: AccountKeysFromLookups | None = None,
    ):
        self.static_account_keys = static_account_keys
        self.account_keys_from_lookups = account_keys_from_lookups

    def __find_key_index(self, key_index_dict: dict[str, int], key: Pubkey) -> int:
        idx = key_index_dict.get(str(key))
        if idx is None:
            raise ValueError(f"Key {key} not found in key_index_dict")
        return idx

    @property
    def length(self) -> int:
        return sum(len(s) for s in self.key_segments())

    def key_segments(self) -> list[Sequence[Pubkey]]:
        # seg 0: static keys
        segments = [self.static_account_keys]
        # seg 1: writable signers
        # seg 2: readonly signers
        if self.account_keys_from_lookups is not None:
            segments.append(self.account_keys_from_lookups.writable)
            segments.append(self.account_keys_from_lookups.readonly)
        return segments

    def get(self, index: int) -> Pubkey:
        """
        Given a flat index, return the corresponding key.
        """
        for segment in self.key_segments():
            if index < len(segment):
                return segment[index]
            index -= len(segment)
        raise IndexError(f"Index {index} is out of bounds")

    def compile_instructions(
        self, instructions: Sequence[Instruction]
    ) -> list[CompiledInstruction]:
        """
        Compile a list of instructions into a list of CompiledInstructions.
        """
        if self.length > U8_MAX + 1:
            raise ValueError("Account index overflow encountered")

        # Build a dict pubkey -> flat index
        flat_keys = [k for seg in self.key_segments() for k in seg]
        key_index_dict = {str(pk): idx for idx, pk in enumerate(flat_keys)}

        compiled_instructions: list[CompiledInstruction] = []
        for ix in instructions:
            # prog id index
            pid_idx = self.__find_key_index(key_index_dict, ix.program_id)
            # account meta's pubkey index
            acc_idx_list = [
                self.__find_key_index(key_index_dict, acct.pubkey)
                for acct in ix.accounts
            ]
            compiled_instruction = CompiledInstruction(
                program_id_index=pid_idx,
                accounts=bytes(acc_idx_list),
                data=ix.data,
            )
            compiled_instructions.append(compiled_instruction)

        return compiled_instructions


class CompiledKeyMeta(BaseModel):
    is_signer: bool
    is_writable: bool
    is_invoked: bool


KeyMetaMap = dict[str, CompiledKeyMeta]


@dataclass
class CompiledKeys:
    """
    Adapted to work with  slightly adapted to work with "wrapped" transaction messaged
    """

    payer: Pubkey
    key_meta_map: KeyMetaMap

    def __init__(self, payer: Pubkey, key_meta_map: KeyMetaMap):
        self.payer = payer
        self.key_meta_map = key_meta_map

    def _drain_keys_found_in_lookup_table(
        self,
        lookup_table_entries: Sequence[Pubkey],
        key_meta_filter: Callable[[CompiledKeyMeta], bool],
    ) -> tuple[Sequence[int], Sequence[Pubkey]]:
        """
        Internal helper to find and remove keys from key_meta_map that
        are present in the lookup_table_entries and match the filter.

        Returns a list of table indexes and a list of drained keys.
        """
        found_indexes: Sequence[int] = []
        drained_keys: Sequence[Pubkey] = []

        # Iterate over a copy of items if modifying the dict during iteration
        # (which self.key_meta_map.delete(address_str) would do)
        for address_str, key_meta in list(self.key_meta_map.items()):
            if key_meta_filter(key_meta):
                key = Pubkey.from_string(address_str)
                try:
                    # Find index of key in lookup_table_entries
                    idx = lookup_table_entries.index(key)
                    assert idx < 256, "Max lookup table index exceeded (must be < 256)"
                    found_indexes.append(idx)
                    drained_keys.append(key)
                    del self.key_meta_map[address_str]
                except ValueError:
                    # Key not found in lookup_table_entries, do nothing
                    pass

        return found_indexes, drained_keys

    @staticmethod
    def compile(
        instructions: Sequence[Instruction],
        payer: Pubkey,
    ) -> "CompiledKeys":
        """
        Compiles a list of instructions and a payer into a CompiledKeys object.

        The main difference from the original solana-web3.js implementation
        is that instruction program_ids are NOT marked as invoked. This allows
        them to be included in Address Lookup Tables for CPIs, optimizing
        transaction size.
        """
        key_meta_map: KeyMetaMap = {}

        def get_or_insert_default(pubkey: Pubkey) -> CompiledKeyMeta:
            address = str(pubkey)  # Pubkey to base58 string for map key
            key_meta = key_meta_map.get(address)
            if key_meta is None:
                key_meta = CompiledKeyMeta(
                    is_signer=False,
                    is_writable=False,
                    is_invoked=False,
                )
                key_meta_map[address] = key_meta
            return key_meta

        payer_key_meta = get_or_insert_default(payer)
        payer_key_meta.is_signer = True
        payer_key_meta.is_writable = True

        for ix in instructions:
            get_or_insert_default(ix.program_id).is_invoked = False

            for account_meta in ix.accounts:
                key_meta = get_or_insert_default(account_meta.pubkey)
                key_meta.is_signer = key_meta.is_signer or account_meta.is_signer
                key_meta.is_writable = key_meta.is_writable or account_meta.is_writable

        return CompiledKeys(payer, key_meta_map)

    def get_message_components(self) -> tuple[MessageHeader, Sequence[Pubkey]]:
        """
        Constructs the message header and a list of static account keys.
        """
        map_entries: Sequence[tuple[str, CompiledKeyMeta]] = list(
            self.key_meta_map.items()
        )
        assert len(map_entries) <= 256, "Max static account keys length exceeded"

        # Sort keys: payer, writable signers, readonly signers,
        # writable non-signers, readonly non-signers
        # The payer should naturally be the first writable signer if logic is correct.

        writable_signers = [
            (address, meta)
            for address, meta in map_entries
            if meta.is_signer and meta.is_writable
        ]
        readonly_signers = [
            (address, meta)
            for address, meta in map_entries
            if meta.is_signer and not meta.is_writable
        ]
        writable_non_signers = [
            (address, meta)
            for address, meta in map_entries
            if not meta.is_signer and meta.is_writable
        ]
        readonly_non_signers = [
            (address, meta)
            for address, meta in map_entries
            if not meta.is_signer and not meta.is_writable
        ]

        header = MessageHeader(
            num_required_signatures=len(writable_signers) + len(readonly_signers),
            num_readonly_signed_accounts=len(readonly_signers),
            num_readonly_unsigned_accounts=len(readonly_non_signers),
        )

        # Sanity checks
        assert len(writable_signers) > 0, "Expected at least one writable signer key"
        assert writable_signers[0][0] == str(self.payer), (
            "Expected first writable signer key to be the fee payer"
        )

        static_account_keys: Sequence[Pubkey] = []

        static_account_keys.extend(
            [Pubkey.from_string(address) for address, _ in writable_signers]
            + [Pubkey.from_string(address) for address, _ in readonly_signers]
            + [Pubkey.from_string(address) for address, _ in writable_non_signers]
            + [Pubkey.from_string(address) for address, _ in readonly_non_signers]
        )

        return header, static_account_keys

    def extract_table_lookup(
        self, lookup_table: AddressLookupTableAccount
    ) -> tuple[MessageAddressTableLookup, AccountKeysFromLookups] | None:
        """
        Attempts to extract account keys into a MessageAddressTableLookup
        if they are found in the provided AddressLookupTableAccount.

        Returns a tuple containing the MessageAddressTableLookup and
        AccountKeysFromLookups if any keys are extracted, otherwise None.
        """
        # Filter for writable keys (not signer, not invoked)
        writable_indexes_list, drained_writable_keys = (
            self._drain_keys_found_in_lookup_table(
                lookup_table.addresses,  # Accessing addresses from state
                lambda key_meta: (
                    not key_meta.is_signer
                    and not key_meta.is_invoked
                    and key_meta.is_writable
                ),
            )
        )

        # Filter for readonly keys (not signer, not invoked)
        readonly_indexes_list, drained_readonly_keys = (
            self._drain_keys_found_in_lookup_table(
                lookup_table.addresses,  # Accessing addresses from state
                lambda key_meta: (
                    not key_meta.is_signer
                    and not key_meta.is_invoked
                    and not key_meta.is_writable
                ),
            )
        )

        if not writable_indexes_list and not readonly_indexes_list:
            return None

        message_address_table_lookup = MessageAddressTableLookup(
            account_key=lookup_table.key,
            writable_indexes=bytes(
                writable_indexes_list
            ),  # Convert list of ints to bytes
            readonly_indexes=bytes(
                readonly_indexes_list
            ),  # Convert list of ints to bytes
        )

        account_keys_from_lookups = AccountKeysFromLookups(
            writable=list(drained_writable_keys),
            readonly=list(drained_readonly_keys),
        )

        return message_address_table_lookup, account_keys_from_lookups
