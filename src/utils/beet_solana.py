from typing import Any, override

from construct import Adapter, Bytes, Container
from solders.pubkey import Pubkey

PUBLIC_KEY_LENGTH = 32


# NOTE: do not touch this, Adapter does not work with generics
class PublicKey(Adapter):  # type: ignore
    """
    construct.Adapter for PublicKey.
    Serializes PublicKey objects to 32 bytes and deserializes 32 bytes
    into PublicKey objects.

    This corresponds to the provided TypeScript `publicKey` beet.
    - `read` is handled by `_decode`.
    - `write` is handled by `_encode`.
    - `byteSize` is implicitly 32 due to `Bytes(32)`.
    """

    def __init__(self) -> None:
        # The underlying construct is 32 raw bytes.
        super().__init__(Bytes(PUBLIC_KEY_LENGTH))  # type: ignore

    @override
    def _encode(  # type: ignore
        self, obj: Pubkey, context: Container[Any] | None, path: str | None
    ) -> bytes:
        """
        Called during building. `obj` is the PublicKey instance.
        """
        try:
            assert isinstance(obj, Pubkey)
        except AssertionError:
            raise TypeError(
                "Expected a PublicKey object, got %s", type(obj).__name__
            ) from None
        return obj.__bytes__()

    def _decode(
        self, obj: bytes, context: Container[Any] | None, path: str | None
    ) -> Pubkey:
        """
        Called during parsing. `obj` is the 32 bytes read from the stream.
        """
        return Pubkey.from_bytes(obj)


PublicKeyConstruct = PublicKey()  # type: ignore
