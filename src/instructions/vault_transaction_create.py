from typing import Annotated

from solders.address_lookup_table_account import AddressLookupTableAccount
from solders.hash import Hash
from solders.instruction import Instruction
from solders.pubkey import Pubkey

from src.generated.instructions.vault_transaction_create import (
    VaultTransactionCreateAccounts,
    VaultTransactionCreateArgs,
)
from src.generated.instructions.vault_transaction_create import (
    vault_transaction_create as vault_transaction_create_instruction,
)
from src.generated.program_id import PROGRAM_ID
from src.generated.types.vault_transaction_create_args import (
    VaultTransactionCreateArgs as VaultTransactionCreateArgsType,
)
from src.generated.types.vault_transaction_create_args import (
    VaultTransactionCreateArgsJSON,
)
from src.pda import get_transaction_pda, get_vault_pda
from src.utils.utils import transaction_message_to_multisig_transaction_message_bytes


def vault_transaction_create(
    multisig_pda: Pubkey,
    transaction_index: int,
    creator: Pubkey,
    rent_payer: Pubkey,
    vault_index: int,
    ephemeral_signers: int,
    transaction_payer: Annotated[Pubkey, "Payer of the transaction for the multisig"],
    transaction_recent_blockhash: Annotated[
        Hash, "Recent blockhash of the transaction for the multisig"
    ],
    transaction_instructions: Annotated[
        list[Instruction], "Instructions of the transaction for the multisig"
    ],
    address_lookup_table_accounts: list[AddressLookupTableAccount],
    memo: str | None,
    program_id: Pubkey | None,
) -> Instruction:
    if program_id is None:
        program_id = PROGRAM_ID

    try:
        assert isinstance(multisig_pda, Pubkey)
        assert isinstance(transaction_index, int)
        assert isinstance(creator, Pubkey)
        assert isinstance(rent_payer, Pubkey)
        assert isinstance(vault_index, int)
        assert isinstance(ephemeral_signers, int)
        assert isinstance(transaction_payer, Pubkey)
        assert isinstance(transaction_recent_blockhash, Hash)
        assert isinstance(transaction_instructions, list)
        assert isinstance(address_lookup_table_accounts, list)
        assert isinstance(memo, str) or memo is None
        assert isinstance(program_id, Pubkey)
    except AssertionError:
        raise ValueError("Invalid argument") from None

    vault_pda = get_vault_pda(multisig_pda, vault_index, program_id)[0]
    tx_pda = get_transaction_pda(multisig_pda, transaction_index, program_id)[0]

    transaction_message_bytes = (
        transaction_message_to_multisig_transaction_message_bytes(
            transaction_payer,
            transaction_recent_blockhash,
            transaction_instructions,
            address_lookup_table_accounts,
            vault_pda,
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
