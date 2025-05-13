from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from ..accounts import PDA
from ..generated.instructions.config_transaction_execute import (
    ConfigTransactionExecuteAccounts,
)
from ..generated.instructions.config_transaction_execute import (
    config_transaction_execute as config_transaction_execute_instruction,
)
from ..generated.program_id import PROGRAM_ID


def config_transaction_execute(
    multisig_pda: Pubkey,
    transaction_index: int,
    member: Pubkey,
    rent_payer: Pubkey | None,
    spending_limits: list[Pubkey],
    program_id: Pubkey | None,
) -> Instruction:
    if program_id is None:
        program_id = PROGRAM_ID

    try:
        assert isinstance(multisig_pda, Pubkey)
        assert isinstance(transaction_index, int)
        assert isinstance(member, Pubkey)
        assert isinstance(rent_payer, Pubkey) or rent_payer is None
        assert isinstance(spending_limits, list)
        assert isinstance(program_id, Pubkey)
    except AssertionError:
        raise ValueError("Invalid argument") from None

    proposal_pda = PDA.get_proposal_pda(multisig_pda, transaction_index, program_id)[0]
    txn_pda = PDA.get_transaction_pda(multisig_pda, transaction_index, program_id)[0]

    anchor_remaining_accounts = [
        AccountMeta(pubkey=spending_limit, is_writable=True, is_signer=False)
        for spending_limit in spending_limits
    ]

    accounts = ConfigTransactionExecuteAccounts(
        multisig=multisig_pda,
        member=member,
        proposal=proposal_pda,
        transaction=txn_pda,
        rent_payer=rent_payer,
    )

    return config_transaction_execute_instruction(
        accounts=accounts,
        program_id=program_id,
        remaining_accounts=anchor_remaining_accounts,
    )
