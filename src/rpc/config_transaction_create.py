from collections.abc import Sequence

from solana.rpc.async_api import AsyncClient
from solana.rpc.types import TxOpts
from solders.pubkey import Pubkey
from solders.rpc.responses import SendTransactionResp
from solders.transaction import Signer

from generated.types.config_action import ConfigActionKind
from src.generated.program_id import PROGRAM_ID
from src.transactions.config_transaction_create import (
    config_transaction_create as create_transaction,
)


async def config_transaction_create(
    connection: AsyncClient,
    fee_payer: Signer,
    multisig_pda: Pubkey,
    transaction_index: int,
    creator: Signer,
    rent_payer: Pubkey,
    actions: list[ConfigActionKind],
    memo: str | None,
    signers: Sequence[Signer] | None,
    send_options: TxOpts | None,
    program_id: Pubkey = PROGRAM_ID,
) -> SendTransactionResp:
    """ """
    assert isinstance(connection, AsyncClient)
    assert isinstance(fee_payer, Signer)
    assert isinstance(multisig_pda, Pubkey)
    assert isinstance(transaction_index, int)
    assert isinstance(creator, Signer)
    assert isinstance(rent_payer, Pubkey)
    assert isinstance(actions, list)
    assert isinstance(memo, str) or memo is None
    assert isinstance(signers, Sequence) or signers is None
    assert isinstance(send_options, TxOpts) or send_options is None
    assert isinstance(program_id, Pubkey) or program_id is None

    blockhash = (await connection.get_latest_blockhash()).value.blockhash

    tx = create_transaction(
        blockhash,
        fee_payer,
        multisig_pda,
        transaction_index,
        creator,
        rent_payer,
        actions,
        memo,
        program_id,
    )

    try:
        return await connection.send_transaction(tx, send_options)
    except Exception as e:
        raise e from None
