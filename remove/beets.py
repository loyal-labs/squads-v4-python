from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from borsh_construct import U8, U16, CStruct
from solders.pubkey import Pubkey

T = TypeVar("T")
V = TypeVar("V")


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
        raise NotImplementedError("This method should be implemented in a subclass")

    @abstractmethod
    def to_fixed_from_value(self, vals: V) -> FixedSizeBeet[T, V]:
        """Creates a FixedSizeBeet by inspecting the value to be written."""
        raise NotImplementedError("This method should be implemented in a subclass")


# Helper functions to "fix" beets, similar to beet.fixBeetFromData/Value
def _fix_beet_from_data(
    element_beet: Beet[T, V], buf: bytes, offset: int
) -> FixedSizeBeet[T, V]:
    if isinstance(element_beet, FixedSizeBeet):
        return element_beet
    if isinstance(element_beet, FixableBeet):
        return element_beet.to_fixed_from_data(buf, offset)
    raise TypeError("Beet type not recognized for fixing from data")


def _fix_beet_from_value(element_beet: Beet[T, V], value: V) -> FixedSizeBeet[T, V]:
    if isinstance(element_beet, FixedSizeBeet):
        return element_beet
    if isinstance(element_beet, FixableBeet):
        return element_beet.to_fixed_from_value(value)
    raise TypeError("Beet type not recognized for fixing from value")


class PublicKeyBeet(FixedSizeBeet[Pubkey, Pubkey]):
    byte_size: int = 32
    description: str = "PublicKey"

    def write(self, buf: bytearray, offset: int, value: Pubkey) -> None:
        buf[offset : offset + self.byte_size] = bytes(value)

    def read(self, buf: bytes, offset: int) -> Pubkey:
        return Pubkey(buf[offset : offset + self.byte_size])


class FixedSizeSmallArrayBeet(FixedSizeBeet[Sequence[T], Sequence[V]], Generic[T, V]):
    def __init__(
        self,
        length_beet_instance: FixedSizeBeet[int, int],
        elements_beets_list: Sequence[FixedSizeBeet[T, V]],
        total_elements_byte_size: int,
    ):
        self._length_beet = length_beet_instance
        self._elements_beets = elements_beets_list
        self.array_length = len(elements_beets_list)  # `length` in TS
        self.byte_size = length_beet_instance.byte_size + total_elements_byte_size

        first_el_desc = (
            "<EMPTY>" if not elements_beets_list else elements_beets_list[0].description
        )
        self.description = (
            f"Array<{first_el_desc}>({self.array_length})"
            f"[ {length_beet_instance.byte_size} + {total_elements_byte_size} ]"
        )

    def write(self, buf: bytearray, offset: int, value: Sequence[V]) -> None:
        assert len(value) == self.array_length

        self._length_beet.write(buf, offset, self.array_length)

        current_offset = offset + self._length_beet.byte_size
        for i in range(self.array_length):
            element_beet = self._elements_beets[i]
            element_beet.write(buf, current_offset, value[i])
            current_offset += element_beet.byte_size

    def read(self, buf: bytes, offset: int) -> Sequence[T]:
        size_from_buffer = self._length_beet.read(buf, offset)
        assert size_from_buffer == self.array_length

        current_offset = offset + self._length_beet.byte_size
        result_array: list[T] = [None] * self.array_length  # type: ignore # preallocate
        for i in range(self.array_length):
            element_beet = self._elements_beets[i]
            # result_array[i] = element_beet.read(buf, current_offset)
            # fix with correct method for sequence
            result_array[i] = element_beet.read(buf, current_offset)

            current_offset += element_beet.byte_size
        return result_array


def fixed_size_small_array(
    length_beet_instance: FixedSizeBeet[int, int],
    elements_beets_list: Sequence[FixedSizeBeet[T, V]],
    total_elements_byte_size: int,
) -> FixedSizeBeet[Sequence[T], Sequence[V]]:
    """
    Factory for a FixedSizeBeet representing an array where:
    - The number of elements is fixed and known.
    - This known length is still written/read using `length_beet_instance`.
    - Elements may have different (but fixed) sizes.
    """
    return FixedSizeSmallArrayBeet(
        length_beet_instance, elements_beets_list, total_elements_byte_size
    )


class SmallArrayFixableBeet(FixableBeet[Sequence[T], Sequence[V]], Generic[T, V]):
    """Internal class for a FixableBeet representing an array with prefixed length."""

    def __init__(
        self,
        length_beet_instance: FixedSizeBeet[int, int],
        element_beet_template: Beet[T, V],
    ):
        assert length_beet_instance
        assert isinstance(length_beet_instance, FixedSizeBeet)
        assert element_beet_template
        assert isinstance(element_beet_template, Beet)

        self._length_beet = length_beet_instance
        self._element_beet_template = element_beet_template
        self.description = "smallArray"

    def to_fixed_from_data(
        self, buf: bytes, offset: int
    ) -> FixedSizeBeet[Sequence[T], Sequence[V]]:
        num_elements = self._length_beet.read(buf, offset)
        elements_data_start_offset = offset + self._length_beet.byte_size
        current_offset_for_element = elements_data_start_offset

        fixed_element_beets: list[FixedSizeBeet[T, V]] = [None] * num_elements  # type: ignore
        for i in range(num_elements):
            try:
                fixed_element = _fix_beet_from_data(
                    self._element_beet_template, buf, current_offset_for_element
                )
                fixed_element_beets[i] = fixed_element
                current_offset_for_element += fixed_element.byte_size
            except TypeError:
                raise TypeError(
                    "Beet type not recognized for fixing from data: %s",
                    self._element_beet_template,
                ) from None
            except Exception as e:
                raise e from None

        total_elements_byte_size = (
            current_offset_for_element - elements_data_start_offset
        )
        return fixed_size_small_array(
            self._length_beet, fixed_element_beets, total_elements_byte_size
        )

    def to_fixed_from_value(
        self, vals: Sequence[V]
    ) -> FixedSizeBeet[Sequence[T], Sequence[V]]:
        """
        Override for the to_fixed_from_value method. Does not accept a single value.

        Creates a FixedSizeBeet by inspecting the value to be written.
        """

        try:
            assert isinstance(vals, list)
        except AssertionError:
            raise TypeError("Value must be a list") from None

        num_elements = len(vals)
        total_elements_byte_size = 0
        fixed_element_beets: list[FixedSizeBeet[T, V]] = [None] * num_elements  # type: ignore # preallocate

        for i in range(num_elements):
            fixed_element = _fix_beet_from_value(self._element_beet_template, vals[i])
            fixed_element_beets[i] = fixed_element
            total_elements_byte_size += fixed_element.byte_size

        return fixed_size_small_array(
            self._length_beet, fixed_element_beets, total_elements_byte_size
        )

    def write(self, buf: bytearray, offset: int, value: Sequence[V]) -> None:
        """plsplspls dont call this directly"""
        fixed_beet = self.to_fixed_from_value(value)
        fixed_beet.write(buf, offset, value)

    def read(self, buf: bytes, offset: int) -> Sequence[T]:
        """plsplspls dont call this directly"""
        fixed_beet = self.to_fixed_from_data(buf, offset)
        return fixed_beet.read(buf, offset)


def small_array(
    length_beet_instance: FixedSizeBeet[int, int], element_beet_template: Beet[T, V]
) -> FixableBeet[Sequence[T], Sequence[V]]:
    """
    Factory for a FixableBeet representing an array where:
    - The number of elements is determined at runtime
    - The length is prefixed using `length_beet_instance`.
    - All elements use the same `element_beet_template`
    """
    return SmallArrayFixableBeet(length_beet_instance, element_beet_template)


# --- Struct Beets ---
@dataclass
class CompiledMsInstruction:
    """Represents a compiled instruction within a multisig transaction message."""

    program_id_index: int
    # NOTE: In TS, accountIndexes and data are Array<number> with beet.u8 elements.
    # So, they are lists of u8 values (0-255).
    account_indexes: Sequence[int]
    data: Sequence[int]


@dataclass
class SquadsMessageAddressTableLookup:
    """
    Represents an address table lookup entry in a message.

    # NOTE: renamed to avoid potential clashes
    """

    account_key: Pubkey
    writable_indexes: Sequence[int]  # List of u8 values
    readonly_indexes: Sequence[int]  # List of u8 values


@dataclass
class SquadsTransactionMessage:
    """
    Represents the custom structure of a transaction message for multisig.

    NOTE: renamed to avoid potential clashes
    """

    num_signers: int
    num_writable_signers: int
    num_writable_non_signers: int
    account_keys: Sequence[Pubkey]
    instructions: Sequence[CompiledMsInstruction]
    address_table_lookups: Sequence[SquadsMessageAddressTableLookup]


class FixedBeetArgsStruct(Generic[T, V], FixedSizeBeet[T, V]):
    """
    Helper for creating FixableBeetArgsStruct instances

    Internal class for a fixed-size struct.
    """

    def __init__(
        self,
        struct_type: type[T],
        field_definitions: Sequence[tuple[str, FixedSizeBeet[Any, Any]]],
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
            # TODO: double check the typing here
            field_value: Any = (
                value[field_name] if is_dict else getattr(value, field_name)
            )
            field_beet.write(buf, current_offset, field_value)
            current_offset += field_beet.byte_size

    def read(self, buf: bytes, offset: int) -> T:
        kwargs: dict[str, Any] = {}
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
        struct_type: type[T],
        args_definitions: Sequence[tuple[str, Beet[Any, Any]]],
        description_str: str,
    ):
        self.struct_type = struct_type  # e.g., the dataclass type
        self.args_definitions = (
            args_definitions  # List of (field_name, original_beet_for_field)
        )
        self.description = description_str

    def to_fixed_from_data(self, buf: bytes, offset: int) -> FixedSizeBeet[T, V]:
        fixed_field_definitions: list[tuple[str, FixedSizeBeet[Any, Any]]] = []
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

        return FixedBeetArgsStruct(
            self.struct_type, fixed_field_definitions, self.description
        )

    def to_fixed_from_value(self, vals: V) -> FixedSizeBeet[T, V]:
        fixed_field_definitions: Sequence[tuple[str, FixedSizeBeet[Any, Any]]] = []
        is_dict = isinstance(vals, dict)

        for field_name, original_field_beet in self.args_definitions:
            # TODO: double check the typing here
            field_val: Any = vals[field_name] if is_dict else getattr(vals, field_name)
            fixed_field_beet = _fix_beet_from_value(original_field_beet, field_val)
            fixed_field_definitions.append((field_name, fixed_field_beet))

        return FixedBeetArgsStruct(
            self.struct_type, fixed_field_definitions, self.description
        )

    def write(self, buf: bytearray, offset: int, value: V) -> None:
        """plsplspls dont call this directly"""
        fixed_beet = self.to_fixed_from_value(value)
        fixed_beet.write(buf, offset, value)

    def read(self, buf: bytes, offset: int) -> T:
        """plsplspls dont call this directly"""
        fixed_beet = self.to_fixed_from_data(buf, offset)
        return fixed_beet.read(buf, offset)


# --- Beets for dataclasses ---
