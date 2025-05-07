from collections.abc import Sequence
from dataclasses import dataclass

from solders.pubkey import Pubkey


@dataclass
class AccountKeysFromLookups:
    writable: Sequence[Pubkey]
    readonly: Sequence[Pubkey]
