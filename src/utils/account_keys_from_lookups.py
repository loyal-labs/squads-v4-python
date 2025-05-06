from collections.abc import Sequence

from pydantic import BaseModel
from solders.pubkey import Pubkey


class AccountKeysFromLookups(BaseModel):
    writable: Sequence[Pubkey]
    readonly: Sequence[Pubkey]
