from solana.rpc.async_api import AsyncClient
from solders.address_lookup_table_account import AddressLookupTableAccount
from solders.instruction import Instruction
from solders.pubkey import Pubkey

from src.generated.accounts.vault_transaction import VaultTransaction
from src.generated.instructions.vault_transaction_execute import (
    VaultTransactionExecuteAccounts,
)
from src.generated.instructions.vault_transaction_execute import (
    vault_transaction_execute as vault_transaction_execute_instruction,
)
from src.generated.program_id import PROGRAM_ID
from src.pda import get_proposal_pda, get_transaction_pda, get_vault_pda
from src.utils.utils import accounts_for_transaction_execute


async def vault_transaction_execute(
    connection: AsyncClient,
    multisig_pda: Pubkey,
    transaction_index: int,
    member: Pubkey,
    program_id: Pubkey | None,
) -> tuple[Instruction, list[AddressLookupTableAccount]]:
    if program_id is None:
        program_id = PROGRAM_ID

    try:
        assert isinstance(connection, AsyncClient)
        assert isinstance(multisig_pda, Pubkey)
        assert isinstance(transaction_index, int)
        assert isinstance(member, Pubkey)
        assert isinstance(program_id, Pubkey)
    except AssertionError:
        raise ValueError("Invalid argument") from None

    proposal_pda = get_proposal_pda(multisig_pda, transaction_index, program_id)[0]
    tx_pda = get_transaction_pda(multisig_pda, transaction_index, program_id)[0]

    tx_acc = await VaultTransaction.fetch(connection, tx_pda)

    assert tx_acc is not None, "Transaction account not found"
    print(f"Transaction message: {tx_acc.message}")

    vault_pda = get_vault_pda(multisig_pda, tx_acc.vault_index, program_id)[0]
    ephemeral_signer_bump_seq = list(tx_acc.ephemeral_signer_bumps)

    account_metas, lookup_table_accs = await accounts_for_transaction_execute(
        connection,
        tx_pda,
        vault_pda,
        tx_acc.message,
        ephemeral_signer_bump_seq,
        program_id,
    )
    print(f"Accounts metas: {account_metas}")

    accs = VaultTransactionExecuteAccounts(
        multisig=multisig_pda,
        proposal=proposal_pda,
        transaction=tx_pda,
        member=member,
    )

    ix = vault_transaction_execute_instruction(
        accs,
        program_id,
        account_metas,
    )

    return ix, lookup_table_accs
