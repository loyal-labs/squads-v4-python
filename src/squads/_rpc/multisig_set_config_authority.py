from collections.abc import Sequence

from solana.rpc.async_api import AsyncClient
from solana.rpc.types import TxOpts
from solders.pubkey import Pubkey
from solders.rpc.responses import SendTransactionResp
from solders.transaction import Signer

from .._internal.utils import get_recent_blockhash
from ..generated.program_id import PROGRAM_ID
from ..transactions import multisig_set_config_authority as create_transaction


async def multisig_set_config_authority(
    connection: AsyncClient,
    fee_payer: Signer,
    multisig_pda: Pubkey,
    config_authority: Pubkey,
    new_config_authority: Pubkey,
    memo: str | None = None,
    signers: Sequence[Signer] | None = None,
    send_options: TxOpts | None = None,
    program_id: Pubkey | None = PROGRAM_ID,
) -> SendTransactionResp:
    """
    Set the config authority for a multisig.
    """
    assert isinstance(connection, AsyncClient)
    assert isinstance(fee_payer, Signer)
    assert isinstance(multisig_pda, Pubkey)
    assert isinstance(config_authority, Pubkey)
    assert isinstance(new_config_authority, Pubkey)
    assert isinstance(memo, str) or memo is None
    assert isinstance(signers, Sequence) or signers is None
    assert isinstance(send_options, TxOpts) or send_options is None
    assert isinstance(program_id, Pubkey) or program_id is None

    tx = create_transaction(
        await get_recent_blockhash(connection),
        fee_payer,
        multisig_pda,
        config_authority,
        new_config_authority,
        memo,
        program_id,
        signers,
    )

    try:
        return await connection.send_transaction(tx, send_options)
    except Exception as e:
        raise e from None
        raise e from None
