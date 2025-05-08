from solders.instruction import Instruction
from solders.pubkey import Pubkey

from src.generated.instructions.config_transaction_create import (
    ConfigTransactionCreateAccounts,
    ConfigTransactionCreateArgs,
)
from src.generated.instructions.config_transaction_create import (
    config_transaction_create as config_transaction_create_instruction,
)
from src.generated.program_id import PROGRAM_ID
from src.generated.types.config_action import ConfigActionKind
from src.generated.types.config_transaction_create_args import (
    ConfigTransactionCreateArgs as ConfigTransactionCreateArgsType,
)
from src.pda import get_transaction_pda


def config_transaction_create(
    multisig_pda: Pubkey,
    transaction_index: int,
    creator: Pubkey,
    rent_payer: Pubkey,
    actions: list[ConfigActionKind],
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
        assert isinstance(actions, list)
        assert isinstance(memo, str | None)
        assert isinstance(program_id, Pubkey)
    except AssertionError:
        raise ValueError("Invalid argument") from None

    txn_pda = get_transaction_pda(multisig_pda, transaction_index, program_id)[0]

    accounts = ConfigTransactionCreateAccounts(
        multisig=multisig_pda,
        transaction=txn_pda,
        creator=creator,
        rent_payer=rent_payer,
    )

    args = ConfigTransactionCreateArgs(
        args=ConfigTransactionCreateArgsType(
            actions=actions,
            memo=memo,
        )
    )

    return config_transaction_create_instruction(
        accounts=accounts, args=args, program_id=program_id
    )
