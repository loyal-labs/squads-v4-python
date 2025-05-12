from solders.instruction import Instruction
from solders.pubkey import Pubkey
from spl.token.instructions import get_associated_token_address

from src.generated.instructions.spending_limit_use import (
    SpendingLimitUseAccounts,
    SpendingLimitUseArgs,
)
from src.generated.instructions.spending_limit_use import (
    spending_limit_use as spending_limit_use_instruction,
)
from src.generated.program_id import PROGRAM_ID
from src.generated.types.spending_limit_use_args import (
    SpendingLimitUseArgs as SpendingLimitUseArgsType,
)
from src.pda import PDA


def spending_limit_use(
    multisig_pda: Pubkey,
    member: Pubkey,
    spending_limit: Pubkey,
    mint: Pubkey,
    vault_index: int,
    amount: int,
    decimals: int,
    destination: Pubkey,
    token_program: Pubkey,
    memo: str | None,
    program_id: Pubkey | None,
) -> Instruction:
    if program_id is None:
        program_id = PROGRAM_ID

    try:
        assert isinstance(multisig_pda, Pubkey)
        assert isinstance(member, Pubkey)
        assert isinstance(spending_limit, Pubkey)
        assert isinstance(mint, Pubkey)
        assert isinstance(vault_index, int)
        assert isinstance(amount, int)
        assert isinstance(decimals, int)
        assert isinstance(destination, Pubkey)
        assert isinstance(token_program, Pubkey)
        assert isinstance(memo, str) or memo is None
        assert isinstance(program_id, Pubkey)
    except AssertionError:
        raise ValueError("Invalid argument") from None

    vault_pda = PDA.get_vault_pda(multisig_pda, vault_index, program_id)[0]
    vault_token_ass_address = get_associated_token_address(
        vault_pda,
        mint,
        token_program,
    )
    vault_token_account = mint and vault_token_ass_address

    destination_token_ass_address = get_associated_token_address(
        destination,
        mint,
        token_program,
    )
    destination_token_account = mint and destination_token_ass_address

    accounts = SpendingLimitUseAccounts(
        multisig=multisig_pda,
        member=member,
        spending_limit=spending_limit,
        vault=vault_pda,
        destination=destination,
        mint=mint,
        vault_token_account=vault_token_account,
        destination_token_account=destination_token_account,
    )

    args = SpendingLimitUseArgs(
        args=SpendingLimitUseArgsType(amount=amount, decimals=decimals, memo=memo),
    )

    return spending_limit_use_instruction(
        accounts=accounts, args=args, program_id=program_id
    )
