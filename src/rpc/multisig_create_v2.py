from solana.rpc.async_api import AsyncClient
from solana.rpc.types import TxOpts
from solders.pubkey import Pubkey
from solders.rpc.responses import SendTransactionResp
from solders.transaction import Signer

from src._internal.utils import get_recent_blockhash
from src.generated.program_id import PROGRAM_ID
from src.generated.types.member import Member
from src.transactions.multisig_create_v2 import multisig_create_v2 as create_transaction


async def multisig_create_v2(
    connection: AsyncClient,
    treasury: Pubkey,
    create_key: Signer,
    creator: Signer,
    multisig_pda: Pubkey,
    threshold: int,
    members: list[Member],
    config_authority: Pubkey | None = None,
    time_lock: int = 0,
    rent_collector: Pubkey | None = None,
    memo: str | None = None,
    send_options: TxOpts | None = None,
    program_id: Pubkey = PROGRAM_ID,
) -> SendTransactionResp:
    """
    Creates a new multisig account.

    - Creates instruction
    - Compiles messageV0
    - Signs transaction
    - Sends transaction

    Must be signed by `creator` and `create_key` before sending it.
    """
    assert isinstance(connection, AsyncClient), "Invalid connection"
    assert isinstance(treasury, Pubkey), "Invalid treasury"
    assert isinstance(create_key, Signer), "Invalid create_key"
    assert isinstance(creator, Signer), "Invalid creator"
    assert isinstance(multisig_pda, Pubkey), "Invalid multisig_pda"
    assert isinstance(config_authority, Pubkey | None), "Invalid config_authority"
    assert isinstance(threshold, int), "Invalid threshold"
    assert isinstance(members, list), "Invalid members"
    assert len(members) > 0, "Invalid members (must be non-empty)"
    assert isinstance(time_lock, int), "Invalid time_lock"
    assert time_lock >= 0, "Invalid time_lock (must be >= 0)"
    assert isinstance(rent_collector, Pubkey | None), "Invalid rent_collector"
    assert isinstance(memo, str | None), "Invalid memo"
    assert isinstance(send_options, TxOpts | None), "Invalid send_options"
    assert isinstance(program_id, Pubkey), "Invalid program_id"

    tx = create_transaction(
        await get_recent_blockhash(connection),
        treasury,
        create_key,
        creator,
        multisig_pda,
        config_authority,
        threshold,
        members,
        time_lock,
        rent_collector,
        memo,
        program_id,
    )

    try:
        return await connection.send_transaction(tx, send_options)
    except Exception as e:
        raise e from None
