from solana.rpc.async_api import AsyncClient
from solana.rpc.types import TxOpts
from solders.pubkey import Pubkey
from solders.rpc.responses import SendTransactionResp
from solders.transaction import Signer

from src.transactions.spending_limit_use import spending_limit_use as create_transaction


async def spending_limit_use(
    connection: AsyncClient,
    fee_payer: Signer,
    member: Signer,
    multisig_pda: Pubkey,
    spending_limit: Pubkey,
    mint: Pubkey,
    vault_index: int,
    amount: int,
    decimals: int,
    destination: Pubkey,
    token_program: Pubkey,
    memo: str | None,
    send_options: TxOpts | None,
    program_id: Pubkey | None,
) -> SendTransactionResp:
    """ """
    try:
        assert isinstance(connection, AsyncClient)
        assert isinstance(fee_payer, Signer)
        assert isinstance(member, Signer)
        assert isinstance(multisig_pda, Pubkey)
        assert isinstance(spending_limit, Pubkey)
        assert isinstance(mint, Pubkey)
        assert isinstance(vault_index, int)
        assert isinstance(amount, int)
        assert isinstance(decimals, int)
        assert isinstance(destination, Pubkey)
        assert isinstance(token_program, Pubkey)
        assert isinstance(memo, str) or memo is None
        assert isinstance(send_options, TxOpts) or send_options is None
        assert isinstance(program_id, Pubkey) or program_id is None
    except AssertionError:
        raise ValueError("Invalid argument") from None

    blockhash = (await connection.get_latest_blockhash()).value.blockhash

    tx = create_transaction(
        blockhash,
        fee_payer.pubkey(),
        multisig_pda,
        member.pubkey(),
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
