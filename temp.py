import enum
import struct
from abc import ABC, abstractmethod
from dataclasses import dataclass
from dataclasses import fields as dataclass_fields
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    List,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
)

# Assuming solders.pubkey.Pubkey is the standard PublicKey type
from solders.pubkey import Pubkey


# Placeholder for invariant, similar to the 'invariant' npm package
def invariant(condition: bool, message: str):
    """Asserts a condition, raising an AssertionError if false."""
    assert condition, message


# Generic type variables
T = TypeVar("T")
V = TypeVar("V")  # V often represents a partial version of T for writing

# --- Basic Beet-like Abstractions ---


class Beet(ABC, Generic[T, V]):
    """Abstract base class for a Beet (serializer/deserializer)."""

    description: str

    @abstractmethod
    def write(self, buf: bytearray, offset: int, value: V) -> None:
        """Writes the value to the buffer at the given offset."""
        pass

    @abstractmethod
    def read(self, buf: bytes, offset: int) -> T:
        """Reads a value from the buffer at the given offset."""
        pass


class FixedSizeBeet(Beet[T, V], ABC):
    """A Beet for types with a fixed byte size."""

    byte_size: int


class FixableBeet(Beet[T, V], ABC):
    """
    A Beet for types whose size can be determined either from the data
    being read or from the value being written. It can be "fixed" into
    a FixedSizeBeet.
    """

    @abstractmethod
    def to_fixed_from_data(self, buf: bytes, offset: int) -> FixedSizeBeet[T, V]:
        """Creates a FixedSizeBeet by inspecting the data in the buffer."""
        pass

    @abstractmethod
    def to_fixed_from_value(self, value: V) -> FixedSizeBeet[T, V]:
        """Creates a FixedSizeBeet by inspecting the value to be written."""
        pass


# Helper functions to "fix" beets, similar to beet.fixBeetFromData/Value
def _fix_beet_from_data(
    element_beet: Union[FixedSizeBeet[T, V], FixableBeet[T, V]], buf: bytes, offset: int
) -> FixedSizeBeet[T, V]:
    if isinstance(element_beet, FixedSizeBeet):
        return element_beet
    if isinstance(element_beet, FixableBeet):
        return element_beet.to_fixed_from_data(buf, offset)
    raise TypeError("Beet type not recognized for fixing from data")


def _fix_beet_from_value(
    element_beet: Union[FixedSizeBeet[T, V], FixableBeet[T, V]], value: V
) -> FixedSizeBeet[T, V]:
    if isinstance(element_beet, FixedSizeBeet):
        return element_beet
    if isinstance(element_beet, FixableBeet):
        return element_beet.to_fixed_from_value(value)
    raise TypeError("Beet type not recognized for fixing from value")


# --- Concrete Basic Beets (Primitives) ---


class U8Beet(FixedSizeBeet[int, int]):
    byte_size: int = 1
    description: str = "u8"

    def write(self, buf: bytearray, offset: int, value: int) -> None:
        struct.pack_into("<B", buf, offset, value)

    def read(self, buf: bytes, offset: int) -> int:
        return struct.unpack_from("<B", buf, offset)[0]


class U16Beet(FixedSizeBeet[int, int]):
    byte_size: int = 2
    description: str = "u16"

    def write(self, buf: bytearray, offset: int, value: int) -> None:
        struct.pack_into("<H", buf, offset, value)

    def read(self, buf: bytes, offset: int) -> int:
        return struct.unpack_from("<H", buf, offset)[0]


beet_u8 = U8Beet()
beet_u16 = U16Beet()


class PublicKeyBeet(FixedSizeBeet[Pubkey, Pubkey]):
    byte_size: int = 32
    description: str = "PublicKey"

    def write(self, buf: bytearray, offset: int, value: Pubkey) -> None:
        buf[offset : offset + self.byte_size] = bytes(value)

    def read(self, buf: bytes, offset: int) -> Pubkey:
        return Pubkey(buf[offset : offset + self.byte_size])


beet_solana_public_key = PublicKeyBeet()


# --- Re-exports from "./generated" ---
# In Python, these would typically be imported from a 'generated' module.
# For this snippet, their existence is noted. If they are classes/functions needed by
# Permissions or other parts, they would need to be defined or imported.
# Example: from .generated import IPermissions as GeneratedIPermissions

# is_proposal_status_active, is_proposal_status_approved, ... (and others)
# are assumed to be available elsewhere if this code is part of a larger project.

# --- Permission Definitions ---


class Permission(enum.IntFlag):
    """Enum representing different permissions with bitmask values."""

    INITIATE = 0b0000_0001
    VOTE = 0b0000_0010
    EXECUTE = 0b0000_0100
    # Python's IntFlag automatically provides iteration and membership testing.


# IPermissions in TypeScript was an interface { mask: number }.
# We'll use this as a type hint for objects expected to have a 'mask'.
class IPermissions(ABC):
    mask: int


class Permissions(IPermissions):
    """Manages a bitmask of permissions."""

    mask: int

    def __init__(self, mask: int):
        self.mask = mask

    @staticmethod
    def from_permissions(permissions: List[Permission]) -> "Permissions":
        """Creates a Permissions object from a list of Permission enum members."""
        mask = 0
        for p_flag in permissions:
            mask |= p_flag.value
        return Permissions(mask)

    @staticmethod
    def all() -> "Permissions":
        """Creates a Permissions object with all defined permissions."""
        mask = 0
        for p_flag in Permission:  # Iterates over all members of the IntFlag
            mask |= p_flag.value
        return Permissions(mask)

    @staticmethod
    def has(permissions_obj: IPermissions, permission_flag: Permission) -> bool:
        """Checks if the given Permissions object (or any object with a mask) has a specific permission."""
        return (permissions_obj.mask & permission_flag.value) == permission_flag.value


# --- Custom Array Beets ---


class _FixedSizeSmallArrayBeet(FixedSizeBeet[List[T], List[V]], Generic[T, V]):
    """Internal class for a fixed-size array with a prefixed length."""

    def __init__(
        self,
        length_beet_instance: FixedSizeBeet[int, int],
        elements_beets_list: List[FixedSizeBeet[T, V]],
        total_elements_byte_size: int,
    ):
        self._length_beet = length_beet_instance
        self._elements_beets = elements_beets_list
        self.array_length = len(elements_beets_list)  # 'length' property in TS beet
        self.byte_size = length_beet_instance.byte_size + total_elements_byte_size

        first_el_desc = (
            "<EMPTY>" if not elements_beets_list else elements_beets_list[0].description
        )
        self.description = (
            f"Array<{first_el_desc}>({self.array_length})"
            f"[ {length_beet_instance.byte_size} + {total_elements_byte_size} ]"
        )

    def write(self, buf: bytearray, offset: int, value: List[V]) -> None:
        invariant(
            len(value) == self.array_length,
            f"array length {len(value)} should match fixed length {self.array_length}",
        )
        self._length_beet.write(buf, offset, self.array_length)

        current_offset = offset + self._length_beet.byte_size
        for i in range(self.array_length):
            element_beet = self._elements_beets[i]
            element_beet.write(buf, current_offset, value[i])
            current_offset += element_beet.byte_size

    def read(self, buf: bytes, offset: int) -> List[T]:
        size_from_buffer = self._length_beet.read(buf, offset)
        invariant(
            size_from_buffer == self.array_length,
            f"array size in buffer {size_from_buffer} should match fixed length {self.array_length}",
        )

        current_offset = offset + self._length_beet.byte_size
        result_array: List[T] = [None] * self.array_length  # type: ignore # preallocate
        for i in range(self.array_length):
            element_beet = self._elements_beets[i]
            result_array[i] = element_beet.read(buf, current_offset)
            current_offset += element_beet.byte_size
        return result_array


def fixed_size_small_array(
    length_beet_instance: FixedSizeBeet[int, int],
    elements_beets_list: List[FixedSizeBeet[T, V]],
    total_elements_byte_size: int,
) -> FixedSizeBeet[List[T], List[V]]:
    """
    Factory for a FixedSizeBeet representing an array where:
    - The number of elements is fixed and known.
    - This known length is still written/read using `length_beet_instance`.
    - Elements may have different (but fixed) sizes.
    """
    return _FixedSizeSmallArrayBeet(
        length_beet_instance, elements_beets_list, total_elements_byte_size
    )


class _SmallArrayFixableBeet(FixableBeet[List[T], List[V]], Generic[T, V]):
    """Internal class for a FixableBeet representing an array with prefixed length."""

    def __init__(
        self,
        length_beet_instance: FixedSizeBeet[int, int],
        element_beet_template: Beet[T, V],
    ):
        self._length_beet = length_beet_instance
        self._element_beet_template = element_beet_template
        self.description = "smallArray"  # Matches TS

    def to_fixed_from_data(
        self, buf: bytes, offset: int
    ) -> FixedSizeBeet[List[T], List[V]]:
        num_elements = self._length_beet.read(buf, offset)
        elements_data_start_offset = offset + self._length_beet.byte_size
        current_offset_for_element = elements_data_start_offset

        fixed_element_beets: List[FixedSizeBeet[T, V]] = [None] * num_elements  # type: ignore
        for i in range(num_elements):
            fixed_element = _fix_beet_from_data(
                self._element_beet_template, buf, current_offset_for_element
            )
            fixed_element_beets[i] = fixed_element
            current_offset_for_element += fixed_element.byte_size

        total_elements_byte_size = (
            current_offset_for_element - elements_data_start_offset
        )
        return fixed_size_small_array(
            self._length_beet, fixed_element_beets, total_elements_byte_size
        )

    def to_fixed_from_value(
        self, values_list: List[V]
    ) -> FixedSizeBeet[List[T], List[V]]:
        invariant(isinstance(values_list, list), f"{values_list} should be a list")

        num_elements = len(values_list)
        total_elements_byte_size = 0
        fixed_element_beets: List[FixedSizeBeet[T, V]] = [None] * num_elements  # type: ignore

        for i in range(num_elements):
            fixed_element = _fix_beet_from_value(
                self._element_beet_template, values_list[i]
            )
            fixed_element_beets[i] = fixed_element
            total_elements_byte_size += fixed_element.byte_size

        return fixed_size_small_array(
            self._length_beet, fixed_element_beets, total_elements_byte_size
        )

    def write(
        self, buf: bytearray, offset: int, value: List[V]
    ) -> None:  # Should not be called directly
        fixed_beet = self.to_fixed_from_value(value)
        fixed_beet.write(buf, offset, value)

    def read(self, buf: bytes, offset: int) -> List[T]:  # Should not be called directly
        fixed_beet = self.to_fixed_from_data(buf, offset)
        return fixed_beet.read(buf, offset)


def small_array(
    length_beet_instance: FixedSizeBeet[int, int], element_beet_template: Beet[T, V]
) -> FixableBeet[List[T], List[V]]:
    """
    Factory for a FixableBeet representing an array where:
    - The number of elements is determined at runtime (read from prefix or from value length).
    - The length is prefixed using `length_beet_instance`.
    - All elements use the same `element_beet_template` (which itself might be fixable).
    """
    return _SmallArrayFixableBeet(length_beet_instance, element_beet_template)


# --- Struct Beets ---


@dataclass
class CompiledMsInstruction:
    """Represents a compiled instruction within a multisig transaction message."""

    program_id_index: int
    # In TS, accountIndexes and data were Array<number> with beet.u8 elements.
    # So, they are lists of u8 values (0-255).
    account_indexes: List[int]
    data: List[int]


@dataclass
class PyMessageAddressTableLookup:  # Renamed to avoid potential clashes
    """Represents an address table lookup entry in a message."""

    account_key: Pubkey
    writable_indexes: List[int]  # List of u8 values
    readonly_indexes: List[int]  # List of u8 values


@dataclass
class PyTransactionMessage:  # Renamed
    """Represents the custom structure of a transaction message for multisig."""

    num_signers: int
    num_writable_signers: int
    num_writable_non_signers: int
    account_keys: List[Pubkey]
    instructions: List[CompiledMsInstruction]
    address_table_lookups: List[PyMessageAddressTableLookup]


# Helper for creating FixableBeetArgsStruct instances
class _FixedBeetArgsStruct(Generic[T, V], FixedSizeBeet[T, V]):
    """Internal class for a fixed-size struct."""

    def __init__(
        self,
        struct_type: Type[T],
        field_definitions: List[Tuple[str, FixedSizeBeet[Any, Any]]],
        description_str: str,
    ):
        self.struct_type = struct_type
        self.field_definitions = field_definitions  # List of (name, fixed_beet)
        self.description = description_str
        self.byte_size = sum(fb.byte_size for _, fb in field_definitions)

    def write(self, buf: bytearray, offset: int, value: V) -> None:
        current_offset = offset
        # value can be a dataclass instance or a dict
        is_dict = isinstance(value, dict)
        for field_name, field_beet in self.field_definitions:
            field_value = value[field_name] if is_dict else getattr(value, field_name)
            field_beet.write(buf, current_offset, field_value)
            current_offset += field_beet.byte_size

    def read(self, buf: bytes, offset: int) -> T:
        kwargs: Dict[str, Any] = {}
        current_offset = offset
        for field_name, field_beet in self.field_definitions:
            kwargs[field_name] = field_beet.read(buf, current_offset)
            current_offset += field_beet.byte_size
        return self.struct_type(**kwargs)


class FixableBeetArgsStruct(Generic[T, V], FixableBeet[T, V]):
    """
    A FixableBeet for struct-like objects (dataclasses in Python).
    Mimics beet.FixableBeetArgsStruct.
    """

    def __init__(
        self,
        struct_type: Type[T],
        args_definitions: List[Tuple[str, Beet[Any, Any]]],
        description_str: str,
    ):
        self.struct_type = struct_type  # e.g., the dataclass type
        self.args_definitions = (
            args_definitions  # List of (field_name, original_beet_for_field)
        )
        self.description = description_str

    def to_fixed_from_data(self, buf: bytes, offset: int) -> FixedSizeBeet[T, V]:
        fixed_field_definitions: List[Tuple[str, FixedSizeBeet[Any, Any]]] = []
        current_offset_for_field = (
            offset  # Fields are laid out sequentially in the buffer
        )

        for field_name, original_field_beet in self.args_definitions:
            fixed_field_beet = _fix_beet_from_data(
                original_field_beet, buf, current_offset_for_field
            )
            fixed_field_definitions.append((field_name, fixed_field_beet))
            current_offset_for_field += (
                fixed_field_beet.byte_size
            )  # Advance buffer pointer for next field

        return _FixedBeetArgsStruct(
            self.struct_type, fixed_field_definitions, self.description
        )

    def to_fixed_from_value(self, value: V) -> FixedSizeBeet[T, V]:
        fixed_field_definitions: List[Tuple[str, FixedSizeBeet[Any, Any]]] = []
        is_dict = isinstance(value, dict)

        for field_name, original_field_beet in self.args_definitions:
            field_val = value[field_name] if is_dict else getattr(value, field_name)
            fixed_field_beet = _fix_beet_from_value(original_field_beet, field_val)
            fixed_field_definitions.append((field_name, fixed_field_beet))

        return _FixedBeetArgsStruct(
            self.struct_type, fixed_field_definitions, self.description
        )

    def write(
        self, buf: bytearray, offset: int, value: V
    ) -> None:  # Should not be called directly
        fixed_beet = self.to_fixed_from_value(value)
        fixed_beet.write(buf, offset, value)

    def read(self, buf: bytes, offset: int) -> T:  # Should not be called directly
        fixed_beet = self.to_fixed_from_data(buf, offset)
        return fixed_beet.read(buf, offset)


# Define beets for the dataclasses

compiled_ms_instruction_beet = FixableBeetArgsStruct(
    CompiledMsInstruction,
    [
        ("program_id_index", beet_u8),
        # accountIndexes: u8-prefixed list of u8s
        ("account_indexes", small_array(beet_u8, beet_u8)),
        # data: u16-prefixed list of u8s
        ("data", small_array(beet_u16, beet_u8)),
    ],
    "CompiledMsInstruction",
)

message_address_table_lookup_beet = FixableBeetArgsStruct(
    PyMessageAddressTableLookup,
    [
        ("account_key", beet_solana_public_key),
        # writableIndexes: u8-prefixed list of u8s
        ("writable_indexes", small_array(beet_u8, beet_u8)),
        # readonlyIndexes: u8-prefixed list of u8s
        ("readonly_indexes", small_array(beet_u8, beet_u8)),
    ],
    "MessageAddressTableLookup",  # Matches TS beet name
)

transaction_message_beet = FixableBeetArgsStruct(
    PyTransactionMessage,
    [
        ("num_signers", beet_u8),
        ("num_writable_signers", beet_u8),
        ("num_writable_non_signers", beet_u8),
        # accountKeys: u8-prefixed list of PublicKeys
        ("account_keys", small_array(beet_u8, beet_solana_public_key)),
        # instructions: u8-prefixed list of CompiledMsInstruction (which itself is fixable)
        ("instructions", small_array(beet_u8, compiled_ms_instruction_beet)),
        # addressTableLookups: u8-prefixed list of MessageAddressTableLookup (fixable)
        (
            "address_table_lookups",
            small_array(beet_u8, message_address_table_lookup_beet),
        ),
    ],
    "TransactionMessage",  # Matches TS beet name
)
