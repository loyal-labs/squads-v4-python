from collections.abc import Sequence
from typing import Annotated

from solana.rpc.async_api import AsyncClient
from solana.rpc.types import TxOpts
from solders.pubkey import Pubkey
from solders.rpc.responses import SendTransactionResp
from solders.transaction import Signer

from src._internal.utils import get_recent_blockhash
from src.generated.program_id import PROGRAM_ID
from src.transactions.config_transaction_execute import (
    config_transaction_execute as create_transaction,
)


async def config_transaction_execute(
    connection: AsyncClient,
    fee_payer: Signer,
    multisig_pda: Pubkey,
    transaction_index: int,
    member: Signer,
    rent_payer: Signer,
    spending_limits: list[Pubkey],
    signers: Sequence[Signer] | None = None,
    send_options: Annotated[
        TxOpts | None,
        (
            "In case the transaction adds or removes SpendingLimits, "
            "pass the array of their Pubkeys here."
        ),
    ] = None,
    program_id: Pubkey = PROGRAM_ID,
) -> SendTransactionResp:
    """Execute a config transaction."""
    assert isinstance(connection, AsyncClient)
    assert isinstance(fee_payer, Signer)
    assert isinstance(multisig_pda, Pubkey)
    assert isinstance(transaction_index, int)
    assert isinstance(member, Signer)
    assert isinstance(rent_payer, Signer)
    assert isinstance(spending_limits, list)
    assert isinstance(signers, Sequence) or signers is None
    assert isinstance(send_options, TxOpts) or send_options is None
    assert isinstance(program_id, Pubkey) or program_id is None

    tx = create_transaction(
        await get_recent_blockhash(connection),
        fee_payer,
        multisig_pda,
        transaction_index,
        member,
        rent_payer,
        spending_limits,
        program_id,
        signers,
    )

    try:
        return await connection.send_transaction(tx, send_options)
    except Exception as e:
        raise e from None
