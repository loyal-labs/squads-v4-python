from typing import Annotated

from solders.address_lookup_table_account import AddressLookupTableAccount
from solders.hash import Hash
from solders.instruction import Instruction
from solders.pubkey import Pubkey

from src._internal.utils import (
    transaction_message_to_multisig_transaction_message_bytes,
)
from src.generated.instructions.vault_transaction_create import (
    VaultTransactionCreateAccounts,
    VaultTransactionCreateArgs,
)
from src.generated.instructions.vault_transaction_create import (
    vault_transaction_create as vault_transaction_create_instruction,
)
from src.generated.types.vault_transaction_create_args import (
    VaultTransactionCreateArgs as VaultTransactionCreateArgsType,
)
from src.generated.types.vault_transaction_create_args import (
    VaultTransactionCreateArgsJSON,
)
from src.pda import PDA


def vault_transaction_create(
    multisig_pda: Pubkey,
    transaction_index: int,
    creator: Pubkey,
    rent_payer: Pubkey | None,
    vault_index: int,
    ephemeral_signers: int,
    transaction_payer: Annotated[Pubkey, "Payer of the transaction for the multisig"],
    transaction_recent_blockhash: Annotated[
        Hash, "Recent blockhash of the transaction for the multisig"
    ],
    transaction_instructions: Annotated[
        list[Instruction], "Instructions of the transaction for the multisig"
    ],
    address_lookup_table_accounts: list[AddressLookupTableAccount] | None,
    memo: str | None,
    program_id: Pubkey,
) -> Instruction:
    assert isinstance(multisig_pda, Pubkey)
    assert isinstance(transaction_index, int)
    assert isinstance(creator, Pubkey)
    assert isinstance(rent_payer, Pubkey) or rent_payer is None
    assert isinstance(vault_index, int)
    assert isinstance(ephemeral_signers, int)
    assert isinstance(transaction_payer, Pubkey)
    assert isinstance(transaction_recent_blockhash, Hash)
    assert isinstance(transaction_instructions, list)
    assert (
        isinstance(address_lookup_table_accounts, list)
        or address_lookup_table_accounts is None
    )
    assert isinstance(memo, str) or memo is None
    assert isinstance(program_id, Pubkey)

    # If rent_payer is not provided, use the creator as the rent payer
    if rent_payer is None:
        rent_payer = creator

    tx_pda = PDA.get_transaction_pda(multisig_pda, transaction_index, program_id)[0]

    transaction_message_bytes = (
        transaction_message_to_multisig_transaction_message_bytes(
            transaction_payer,
            transaction_recent_blockhash,
            transaction_instructions,
            address_lookup_table_accounts,
        )
    )

    accounts = VaultTransactionCreateAccounts(
        multisig=multisig_pda,
        transaction=tx_pda,
        creator=creator,
        rent_payer=rent_payer,
    )
    args = VaultTransactionCreateArgsJSON(
        vault_index=vault_index,
        ephemeral_signers=ephemeral_signers,
        transaction_message=list(transaction_message_bytes),
        memo=memo,
    )

    args = VaultTransactionCreateArgs(
        args=VaultTransactionCreateArgsType.from_json(args)
    )

    return vault_transaction_create_instruction(
        accounts=accounts, args=args, program_id=program_id
    )
