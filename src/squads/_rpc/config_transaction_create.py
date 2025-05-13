from collections.abc import Sequence
from typing import Annotated

from solana.rpc.async_api import AsyncClient
from solana.rpc.types import TxOpts
from solders.pubkey import Pubkey
from solders.rpc.responses import SendTransactionResp
from solders.transaction import Signer

from .._internal.utils import get_recent_blockhash
from ..generated.program_id import PROGRAM_ID
from ..generated.types.config_action import ConfigActionKind
from ..transactions import config_transaction_create as create_transaction


async def config_transaction_create(
    connection: AsyncClient,
    fee_payer: Signer,
    multisig_pda: Pubkey,
    transaction_index: int,
    # Member of the multisig that is creating the transaction.
    creator: Annotated[Pubkey, "Member creating the transaction"],
    actions: list[ConfigActionKind],
    # Payer for the txn account rent. If not provided, `creator` is used.
    rent_payer: Annotated[Pubkey | None, "Payer for the txn account rent"] = None,
    memo: str | None = None,
    signers: Sequence[Signer] | None = None,
    send_options: TxOpts | None = None,
    program_id: Pubkey = PROGRAM_ID,
) -> SendTransactionResp:
    """
    Needs to be signed by config authority and fee payer before sending it.
    """
    assert isinstance(connection, AsyncClient)
    assert isinstance(fee_payer, Signer)
    assert isinstance(multisig_pda, Pubkey)
    assert isinstance(transaction_index, int)
    assert isinstance(creator, Pubkey)
    assert isinstance(rent_payer, Pubkey)
    assert isinstance(actions, list)
    assert isinstance(memo, str) or memo is None
    assert isinstance(signers, Sequence) or signers is None
    assert isinstance(send_options, TxOpts) or send_options is None
    assert isinstance(program_id, Pubkey) or program_id is None

    tx = create_transaction(
        await get_recent_blockhash(connection),
        fee_payer,
        multisig_pda,
        transaction_index,
        creator,
        rent_payer,
        actions,
        memo,
        program_id,
        signers,
    )

    try:
        return await connection.send_transaction(tx, send_options)
    except Exception as e:
        raise e from None
