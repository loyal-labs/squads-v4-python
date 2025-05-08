from collections.abc import Sequence

from solana.rpc.async_api import AsyncClient
from solana.rpc.types import TxOpts
from solders.pubkey import Pubkey
from solders.rpc.responses import SendTransactionResp
from solders.transaction import Signer

from src.transactions.vault_transaction_execute import (
    vault_transaction_execute as create_transaction,
)


async def vault_transaction_execute(
    connection: AsyncClient,
    fee_payer: Signer,
    multisig_pda: Pubkey,
    transaction_index: int,
    member: Pubkey,
    signers: Sequence[Signer],
    send_options: TxOpts,
    program_id: Pubkey | None,
) -> SendTransactionResp:
    """ """
    try:
        assert isinstance(connection, AsyncClient)
        assert isinstance(fee_payer, Signer)
        assert isinstance(multisig_pda, Pubkey)
        assert isinstance(transaction_index, int)
        assert isinstance(member, Pubkey)
        assert isinstance(signers, Sequence)
        assert isinstance(send_options, TxOpts)
        assert isinstance(program_id, Pubkey) or program_id is None
    except AssertionError:
        raise ValueError("Invalid argument") from None

    blockhash = (await connection.get_latest_blockhash()).value.blockhash

    tx = await create_transaction(
        connection,
        blockhash,
        fee_payer.pubkey(),
        multisig_pda,
        transaction_index,
        member,
        program_id,
    )

    try:
        return await connection.send_transaction(tx)
    except Exception as e:
        raise e from None
