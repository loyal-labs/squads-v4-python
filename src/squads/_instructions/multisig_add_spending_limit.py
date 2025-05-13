from solders.instruction import Instruction
from solders.pubkey import Pubkey

from ..generated.instructions.multisig_add_spending_limit import (
    MultisigAddSpendingLimitAccounts,
    MultisigAddSpendingLimitArgs,
)
from ..generated.instructions.multisig_add_spending_limit import (
    multisig_add_spending_limit as multisig_add_spending_limit_instruction,
)
from ..generated.program_id import PROGRAM_ID
from ..generated.types.multisig_add_spending_limit_args import (
    MultisigAddSpendingLimitArgs as MultisigAddSpendingLimitArgsType,
)
from ..generated.types.period import PeriodKind


def multisig_add_spending_limit(
    multisig_pda: Pubkey,
    config_authority: Pubkey,
    spending_limit: Pubkey,
    rent_payer: Pubkey,
    create_key: Pubkey,
    vault_index: int,
    mint: Pubkey,
    amount: int,
    period: PeriodKind,
    members: list[Pubkey],
    destinations: list[Pubkey],
    memo: str | None,
    program_id: Pubkey | None,
) -> Instruction:
    if program_id is None:
        program_id = PROGRAM_ID

    try:
        assert isinstance(multisig_pda, Pubkey)
        assert isinstance(config_authority, Pubkey)
        assert isinstance(rent_payer, Pubkey)
        assert isinstance(create_key, Pubkey)
        assert isinstance(vault_index, int)
        assert isinstance(mint, Pubkey)
        assert isinstance(amount, int)
        assert isinstance(period, PeriodKind)
        assert isinstance(members, list)
        assert isinstance(destinations, list)
        assert isinstance(memo, str | None)
        assert isinstance(program_id, Pubkey)
    except AssertionError:
        raise ValueError("Invalid argument") from None

    accounts = MultisigAddSpendingLimitAccounts(
        multisig=multisig_pda,
        spending_limit=spending_limit,
        config_authority=config_authority,
        rent_payer=rent_payer,
    )

    args = MultisigAddSpendingLimitArgs(
        args=MultisigAddSpendingLimitArgsType(
            create_key=create_key,
            vault_index=vault_index,
            mint=mint,
            amount=amount,
            period=period,
            members=members,
            destinations=destinations,
            memo=memo,
        )
    )

    return multisig_add_spending_limit_instruction(
        accounts=accounts, args=args, program_id=program_id
    )
