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
from src.generated.types.spending_limit_use_args import (
    SpendingLimitUseArgs as SpendingLimitUseArgsType,
)
from src.pda import PDA


def spending_limit_use(
    multisig_pda: Pubkey,
    member: Pubkey,
    spending_limit: Pubkey,
    mint: Pubkey | None,
    vault_index: int,
    amount: int,
    decimals: int,
    destination: Pubkey,
    token_program: Pubkey | None,
    memo: str | None,
    program_id: Pubkey,
) -> Instruction:
    assert isinstance(multisig_pda, Pubkey)
    assert isinstance(member, Pubkey)
    assert isinstance(spending_limit, Pubkey)
    assert isinstance(mint, Pubkey) or mint is None
    assert isinstance(vault_index, int)
    assert isinstance(amount, int)
    assert isinstance(decimals, int)
    assert isinstance(destination, Pubkey)
    assert isinstance(token_program, Pubkey) or token_program is None
    assert isinstance(memo, str) or memo is None
    assert isinstance(program_id, Pubkey)

    vault_pda = PDA.get_vault_pda(multisig_pda, vault_index, program_id)[0]

    if mint is not None:
        if token_program is None:
            vault_token_ass_address = get_associated_token_address(
                vault_pda,
                mint,
            )
            destination_token_ass_address = get_associated_token_address(
                destination,
                mint,
            )
        else:
            vault_token_ass_address = get_associated_token_address(
                vault_pda,
                mint,
                token_program,
            )
            destination_token_ass_address = get_associated_token_address(
                destination,
                mint,
                token_program,
            )
    else:
        vault_token_ass_address = None
        destination_token_ass_address = None

    accounts = SpendingLimitUseAccounts(
        multisig=multisig_pda,
        member=member,
        spending_limit=spending_limit,
        vault=vault_pda,
        destination=destination,
        mint=mint,
        vault_token_account=vault_token_ass_address,
        destination_token_account=destination_token_ass_address,
    )

    args = SpendingLimitUseArgs(
        args=SpendingLimitUseArgsType(amount=amount, decimals=decimals, memo=memo),
    )

    return spending_limit_use_instruction(
        accounts=accounts, args=args, program_id=program_id
    )
