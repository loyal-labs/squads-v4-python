from typing import Annotated

from solana.rpc.async_api import AsyncClient
from solana.rpc.types import TxOpts
from solders.pubkey import Pubkey
from solders.rpc.responses import SendTransactionResp
from solders.transaction import Signer

from src._internal.utils import get_recent_blockhash
from src.generated.program_id import PROGRAM_ID
from src.transactions.proposal_create import proposal_create as create_transaction


async def proposal_create(
    connection: AsyncClient,
    fee_payer: Signer,
    creator: Annotated[Signer, "Member of multisig creating the proposal"],
    multisig_pda: Pubkey,
    transaction_index: int,
    rent_payer: Annotated[Signer | None, "If not provided, `creator` is used"] = None,
    is_draft: bool = False,
    program_id: Pubkey = PROGRAM_ID,
    send_options: TxOpts | None = None,
) -> SendTransactionResp:
    """Create a proposal."""
    assert isinstance(connection, AsyncClient)
    assert isinstance(fee_payer, Signer)
    assert isinstance(creator, Signer)
    assert isinstance(rent_payer, Signer) or rent_payer is None
    assert isinstance(multisig_pda, Pubkey)
    assert isinstance(transaction_index, int)
    assert isinstance(is_draft, bool)
    assert isinstance(program_id, Pubkey)
    assert isinstance(send_options, TxOpts) or send_options is None

    tx = create_transaction(
        await get_recent_blockhash(connection),
        fee_payer,
        multisig_pda,
        transaction_index,
        creator,
        rent_payer,
        is_draft,
        program_id,
    )

    try:
        return await connection.send_transaction(tx, send_options)
    except Exception as e:
        raise e from None
