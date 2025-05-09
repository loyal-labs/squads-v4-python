from typing import Annotated

from solana.rpc.async_api import AsyncClient
from solana.rpc.types import TxOpts
from solders.address_lookup_table_account import AddressLookupTableAccount
from solders.hash import Hash
from solders.instruction import Instruction
from solders.pubkey import Pubkey
from solders.rpc.responses import SendTransactionResp
from solders.transaction import Signer

from src.transactions.vault_transaction_create import (
    vault_transaction_create as create_transaction,
)


async def vault_transaction_create(
    connection: AsyncClient,
    fee_payer: Signer,
    multisig_pda: Pubkey,
    transaction_index: int,
    creator: Annotated[Signer, "Member of multisig creating the transaction"],
    rent_payer: Annotated[Signer, "If not provided, `creator` is used"],
    vault_index: int,
    ephemeral_signers: Annotated[int, "Number of ephmeral signing PDA for txn"],
    transaction_payer: Annotated[Pubkey, "Payer of the transaction for the multisig"],
    transaction_recent_blockhash: Annotated[
        Hash, "Recent blockhash of the transaction for the multisig"
    ],
    transaction_instructions: Annotated[
        list[Instruction], "Instructions of the transaction for the multisig"
    ],
    address_lookup_table_accounts: list[AddressLookupTableAccount],
    memo: str | None,
    signers: list[Signer] | None,
    send_options: TxOpts | None,
    program_id: Pubkey | None,
) -> SendTransactionResp:
    """ """
    try:
        assert isinstance(connection, AsyncClient)
        assert isinstance(fee_payer, Signer)
        assert isinstance(creator, Signer)
        assert isinstance(rent_payer, Signer)
        assert isinstance(multisig_pda, Pubkey)
        assert isinstance(transaction_index, int)
        assert isinstance(vault_index, int)
        assert isinstance(ephemeral_signers, int)
        assert isinstance(transaction_payer, Pubkey)
        assert isinstance(transaction_recent_blockhash, Hash)
        assert isinstance(transaction_instructions, list)
        assert isinstance(address_lookup_table_accounts, list)
        assert isinstance(memo, str) or memo is None
        assert isinstance(signers, list) or signers is None
        assert isinstance(send_options, TxOpts) or send_options is None
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
        rent_payer.pubkey(),
        vault_index,
        ephemeral_signers,
        transaction_payer,
        transaction_recent_blockhash,
        transaction_instructions,
        address_lookup_table_accounts,
        memo,
        program_id,
    )
    try:
        return await connection.send_transaction(tx, send_options)
    except Exception as e:
        raise e from None
