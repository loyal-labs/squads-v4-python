from solders.instruction import Instruction
from solders.pubkey import Pubkey

from src.generated.instructions.multisig_change_threshold import (
    MultisigChangeThresholdAccounts,
    MultisigChangeThresholdArgs,
)
from src.generated.instructions.multisig_change_threshold import (
    multisig_change_threshold as multisig_change_threshold_instruction,
)
from src.generated.program_id import PROGRAM_ID
from src.generated.types.multisig_change_threshold_args import (
    MultisigChangeThresholdArgs as MultisigChangeThresholdArgsType,
)


def multisig_change_threshold(
    multisig_pda: Pubkey,
    config_authority: Pubkey,
    rent_payer: Pubkey,
    new_threshold: int,
    memo: str | None,
    program_id: Pubkey | None,
) -> Instruction:
    if program_id is None:
        program_id = PROGRAM_ID

    try:
        assert isinstance(multisig_pda, Pubkey)
        assert isinstance(config_authority, Pubkey)
        assert isinstance(rent_payer, Pubkey)
        assert isinstance(new_threshold, int)
        assert isinstance(memo, str | None)
        assert isinstance(program_id, Pubkey)
    except AssertionError:
        raise ValueError("Invalid argument") from None

    accounts = MultisigChangeThresholdAccounts(
        multisig=multisig_pda,
        config_authority=config_authority,
        rent_payer=rent_payer,
    )

    args = MultisigChangeThresholdArgs(
        args=MultisigChangeThresholdArgsType(
            new_threshold=new_threshold,
            memo=memo,
        )
    )

    return multisig_change_threshold_instruction(
        accounts=accounts, args=args, program_id=program_id
    )
