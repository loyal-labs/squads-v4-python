from collections.abc import Sequence

from solana.rpc.async_api import AsyncClient
from solana.rpc.types import TxOpts
from solders.pubkey import Pubkey
from solders.rpc.responses import SendTransactionResp
from solders.transaction import Signer

from src.transactions.multisig_set_config_authority import (
    multisig_set_config_authority as create_transaction,
)


async def multisig_set_config_authority(
    connection: AsyncClient,
    fee_payer: Signer,
    multisig_pda: Pubkey,
    config_authority: Pubkey,
    new_config_authority: Pubkey,
    memo: str | None,
    signers: Sequence[Signer] | None,
    send_options: TxOpts | None,
    program_id: Pubkey | None,
) -> SendTransactionResp:
    """ """
    try:
        assert isinstance(connection, AsyncClient)
        assert isinstance(fee_payer, Signer)
        assert isinstance(multisig_pda, Pubkey)
        assert isinstance(config_authority, Pubkey)
        assert isinstance(new_config_authority, Pubkey)
        assert isinstance(memo, str) or memo is None
        assert isinstance(signers, Sequence) or signers is None
        assert isinstance(send_options, TxOpts) or send_options is None
        assert isinstance(program_id, Pubkey) or program_id is None
    except AssertionError:
        raise ValueError("Invalid argument") from None

    blockhash = (await connection.get_latest_blockhash()).value.blockhash

    tx = create_transaction(
        blockhash,
        fee_payer.pubkey(),
        multisig_pda,
        config_authority,
        new_config_authority,
        memo,
        program_id,
    )

    try:
        return await connection.send_transaction(tx, send_options)
    except Exception as e:
        raise e from None
