from collections.abc import Sequence

from solana.rpc.async_api import AsyncClient
from solana.rpc.types import TxOpts
from solders.pubkey import Pubkey
from solders.rpc.responses import SendTransactionResp
from solders.transaction import Signer

from generated.types.period import PeriodKind
from src.generated.program_id import PROGRAM_ID
from src.transactions.multisig_add_spending_limit import (
    multisig_add_spending_limit as create_transaction,
)


async def multisig_add_spending_limit(
    connection: AsyncClient,
    fee_payer: Signer,
    multisig_pda: Pubkey,
    config_authority: Pubkey,
    spending_limit: Pubkey,
    rent_payer: Signer,
    create_key: Pubkey,
    vault_index: int,
    mint: Pubkey,
    amount: int,
    period: PeriodKind,
    members: list[Pubkey],
    destinations: list[Pubkey],
    memo: str | None = None,
    signers: Sequence[Signer] | None = None,
    send_options: TxOpts | None = None,
    program_id: Pubkey | None = PROGRAM_ID,
) -> SendTransactionResp:
    """ """
    assert isinstance(connection, AsyncClient)
    assert isinstance(fee_payer, Signer)
    assert isinstance(multisig_pda, Pubkey)
    assert isinstance(config_authority, Pubkey)
    assert isinstance(rent_payer, Signer)
    assert isinstance(create_key, Pubkey)
    assert isinstance(vault_index, int)
    assert isinstance(mint, Pubkey)
    assert isinstance(amount, int)
    assert isinstance(period, PeriodKind)
    assert isinstance(members, list)
    assert isinstance(destinations, list)
    assert isinstance(memo, str) or memo is None
    assert isinstance(signers, Sequence) or signers is None
    assert isinstance(send_options, TxOpts) or send_options is None
    assert isinstance(program_id, Pubkey)

    blockhash = (await connection.get_latest_blockhash()).value.blockhash

    tx = create_transaction(
        blockhash,
        fee_payer,
        multisig_pda,
        config_authority,
        spending_limit,
        rent_payer,
        create_key,
        vault_index,
        mint,
        amount,
        period,
        members,
        destinations,
        memo,
        program_id,
        signers,
    )

    try:
        return await connection.send_transaction(tx, send_options)
    except Exception as e:
        raise e from None
