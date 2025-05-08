from typing import Annotated

from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey
from solders.rpc.responses import SendTransactionResp
from solders.transaction import Signer

from src.transactions.proposal_create import proposal_create as create_transaction


async def proposal_create(
    connection: AsyncClient,
    fee_payer: Signer,
    creator: Annotated[Signer, "Member of multisig creating the proposal"],
    rent_payer: Annotated[Signer | None, "If not provided, `creator` is used"],
    multisig_pda: Pubkey,
    transaction_index: int,
    is_draft: bool | None,
    program_id: Pubkey | None,
) -> SendTransactionResp:
    """ """
    try:
        assert isinstance(connection, AsyncClient)
        assert isinstance(fee_payer, Signer)
        assert isinstance(creator, Signer)
        assert isinstance(rent_payer, Pubkey) or rent_payer is None
        assert isinstance(multisig_pda, Pubkey)
        assert isinstance(transaction_index, int)
        assert isinstance(is_draft, bool) or is_draft is None
        assert isinstance(program_id, Pubkey) or program_id is None
    except AssertionError:
        raise ValueError("Invalid argument") from None

    blockhash = (await connection.get_latest_blockhash()).value.blockhash

    tx = create_transaction(
        blockhash,
        fee_payer.pubkey(),
        multisig_pda,
        transaction_index,
        creator.pubkey(),
        rent_payer.pubkey() if rent_payer else None,
        is_draft,
        program_id,
    )

    try:
        return await connection.send_transaction(tx)
    except Exception as e:
        raise e from None
