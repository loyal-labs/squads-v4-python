from collections.abc import Sequence

from solana.rpc.async_api import AsyncClient
from solders.hash import Hash
from solders.message import MessageV0
from solders.pubkey import Pubkey
from solders.transaction import Signer, VersionedTransaction

from ..instructions import vault_transaction_execute as create_instruction


async def vault_transaction_execute(
    connection: AsyncClient,
    blockhash: Hash,
    fee_payer: Signer,
    multisig_pda: Pubkey,
    transaction_index: int,
    member: Pubkey,
    program_id: Pubkey,
    signers: Sequence[Signer] | None,
) -> VersionedTransaction:
    """
    Returns `VersionedTransaction` that needs to be
    signed by `member` and `fee_payer` before sending it.
    """
    assert isinstance(blockhash, Hash)
    assert isinstance(connection, AsyncClient)
    assert isinstance(fee_payer, Signer)
    assert isinstance(multisig_pda, Pubkey)
    assert isinstance(transaction_index, int)
    assert isinstance(member, Pubkey)
    assert isinstance(program_id, Pubkey)
    assert isinstance(signers, Sequence) or signers is None

    ix, lookup_table_accounts = await create_instruction(
        connection,
        multisig_pda,
        transaction_index,
        member,
        program_id,
    )

    message_v0 = MessageV0.try_compile(
        fee_payer.pubkey(),
        [ix],
        lookup_table_accounts,
        blockhash,
    )
    signers_list = [fee_payer]
    if signers is not None:
        signers_list.extend(signers)

    versioned_tx = VersionedTransaction(message_v0, signers_list)

    return versioned_tx
    return versioned_tx
