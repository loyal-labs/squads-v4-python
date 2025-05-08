from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey
from solders.transaction import Signer

from src.generated.types.member import Member
from src.transactions.multisig_create_v2 import multisig_create_v2 as create_transaction


async def multisig_create_v2(
    connection: AsyncClient,
    treasury: Pubkey,
    create_key: Signer,
    creator: Signer,
    multisig: Pubkey,
    config_authority: Pubkey | None,
    threshold: int,
    members: list[Member],
    time_lock: int,
    rent_collector: Pubkey | None,
    memo: str | None,
    program_id: Pubkey,
):
    blockhash = (await connection.get_latest_blockhash()).value.blockhash

    tx = create_transaction(
        blockhash,
        treasury,
        create_key.pubkey(),
        creator.pubkey(),
        multisig,
        config_authority,
        threshold,
        members,
        time_lock,
        rent_collector,
        memo,
        program_id,
    )

    tx.sign([creator, create_key], blockhash)

    return await connection.send_transaction(tx)
