from typing import Annotated

from solana.rpc.async_api import AsyncClient
from solana.rpc.types import TxOpts
from solders.pubkey import Pubkey
from solders.rpc.responses import SendTransactionResp
from solders.transaction import Signer

from .._internal.utils import get_recent_blockhash
from ..generated.program_id import PROGRAM_ID
from ..transactions import spending_limit_use as create_transaction


async def spending_limit_use(
    connection: AsyncClient,
    fee_payer: Signer,
    member: Signer,
    multisig_pda: Pubkey,
    spending_limit: Pubkey,
    vault_index: int,
    amount: int,
    decimals: int,
    destination: Pubkey,
    token_program: Pubkey | None = None,
    mint: Annotated[
        Pubkey | None,
        ("Provide if `spendingLimit` is for an SPL token, omit if it's for SOL."),
    ] = None,
    memo: str | None = None,
    send_options: TxOpts | None = None,
    program_id: Pubkey = PROGRAM_ID,
) -> SendTransactionResp:
    """
    Use a spending limit.

    Must be signed by `feePayer` and `member`.
    """
    assert isinstance(connection, AsyncClient)
    assert isinstance(fee_payer, Signer)
    assert isinstance(member, Signer)
    assert isinstance(multisig_pda, Pubkey)
    assert isinstance(spending_limit, Pubkey)
    assert isinstance(mint, Pubkey) or mint is None
    assert isinstance(vault_index, int)
    assert isinstance(amount, int)
    assert isinstance(decimals, int)
    assert isinstance(destination, Pubkey)
    assert isinstance(token_program, Pubkey) or token_program is None
    assert isinstance(memo, str) or memo is None
    assert isinstance(send_options, TxOpts) or send_options is None
    assert isinstance(program_id, Pubkey)

    tx = create_transaction(
        await get_recent_blockhash(connection),
        fee_payer,
        multisig_pda,
        member,
        spending_limit,
        mint,
        vault_index,
        amount,
        decimals,
        destination,
        token_program,
        memo,
        program_id,
    )

    try:
        return await connection.send_transaction(tx, send_options)
    except Exception as e:
        raise e from None
