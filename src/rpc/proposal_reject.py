from solana.rpc.async_api import AsyncClient
from solana.rpc.types import TxOpts
from solders.pubkey import Pubkey
from solders.rpc.responses import SendTransactionResp
from solders.transaction import Signer

from src._internal.utils import get_recent_blockhash
from src.generated.program_id import PROGRAM_ID
from src.transactions.proposal_reject import proposal_reject as create_transaction


async def proposal_reject(
    connection: AsyncClient,
    fee_payer: Signer,
    member: Signer,
    multisig_pda: Pubkey,
    transaction_index: int,
    memo: str | None = None,
    send_options: TxOpts | None = None,
    program_id: Pubkey = PROGRAM_ID,
) -> SendTransactionResp:
    """ """
    assert isinstance(connection, AsyncClient)
    assert isinstance(fee_payer, Signer)
    assert isinstance(member, Signer)
    assert isinstance(multisig_pda, Pubkey)
    assert isinstance(transaction_index, int)
    assert isinstance(memo, str) or memo is None
    assert isinstance(send_options, TxOpts) or send_options is None
    assert isinstance(program_id, Pubkey)

    tx = create_transaction(
        await get_recent_blockhash(connection),
        fee_payer,
        multisig_pda,
        transaction_index,
        member,
        memo,
        program_id,
    )

    try:
        return await connection.send_transaction(tx, send_options)
    except Exception as e:
        raise e from None
