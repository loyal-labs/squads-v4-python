from solders.instruction import Instruction
from solders.pubkey import Pubkey

from src.generated.instructions.multisig_remove_spending_limit import (
    MultisigRemoveSpendingLimitAccounts,
    MultisigRemoveSpendingLimitArgs,
)
from src.generated.instructions.multisig_remove_spending_limit import (
    multisig_remove_spending_limit as multisig_remove_spending_limit_instruction,
)
from src.generated.program_id import PROGRAM_ID
from src.generated.types.multisig_remove_spending_limit_args import (
    MultisigRemoveSpendingLimitArgs as MultisigRemoveSpendingLimitArgsType,
)


def multisig_remove_spending_limit(
    multisig_pda: Pubkey,
    config_authority: Pubkey,
    spending_limit: Pubkey,
    rent_collector: Pubkey,
    memo: str | None,
    program_id: Pubkey | None,
) -> Instruction:
    if program_id is None:
        program_id = PROGRAM_ID

    try:
        assert isinstance(multisig_pda, Pubkey)
        assert isinstance(config_authority, Pubkey)
        assert isinstance(spending_limit, Pubkey)
        assert isinstance(rent_collector, Pubkey)
        assert isinstance(memo, str | None)
        assert isinstance(program_id, Pubkey)
    except AssertionError:
        raise ValueError("Invalid argument") from None

    accounts = MultisigRemoveSpendingLimitAccounts(
        multisig=multisig_pda,
        config_authority=config_authority,
        spending_limit=spending_limit,
        rent_collector=rent_collector,
    )

    args = MultisigRemoveSpendingLimitArgs(
        args=MultisigRemoveSpendingLimitArgsType(
            memo=memo,
        )
    )

    return multisig_remove_spending_limit_instruction(
        accounts=accounts, args=args, program_id=program_id
    )
