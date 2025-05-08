from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey
from solders.transaction import Signer

from src.generated.program_id import PROGRAM_ID
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
    program_id: Pubkey = PROGRAM_ID,
):
    try:
        assert isinstance(connection, AsyncClient)
        assert isinstance(treasury, Pubkey)
        assert isinstance(create_key, Signer)
        assert isinstance(creator, Signer)
        assert isinstance(multisig, Pubkey)
        assert isinstance(config_authority, Pubkey | None)
        assert isinstance(threshold, int)
        assert isinstance(members, list)
        assert isinstance(time_lock, int)
        assert isinstance(rent_collector, Pubkey | None)
        assert isinstance(memo, str | None)
        assert isinstance(program_id, Pubkey)
    except AssertionError:
        raise ValueError("Invalid argument") from None

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
