from solders.instruction import Instruction
from solders.pubkey import Pubkey

from ..generated.instructions.multisig_set_config_authority import (
    MultisigSetConfigAuthorityAccounts,
    MultisigSetConfigAuthorityArgs,
)
from ..generated.instructions.multisig_set_config_authority import (
    multisig_set_config_authority as multisig_set_config_authority_instruction,
)
from ..generated.program_id import PROGRAM_ID
from ..generated.types.multisig_set_config_authority_args import (
    MultisigSetConfigAuthorityArgs as MultisigSetConfigAuthorityArgsType,
)


def multisig_set_config_authority(
    multisig_pda: Pubkey,
    config_authority: Pubkey,
    new_config_authority: Pubkey,
    memo: str | None,
    program_id: Pubkey | None,
) -> Instruction:
    if program_id is None:
        program_id = PROGRAM_ID

    try:
        assert isinstance(multisig_pda, Pubkey)
        assert isinstance(config_authority, Pubkey)
        assert isinstance(new_config_authority, Pubkey)
        assert isinstance(memo, str | None)
        assert isinstance(program_id, Pubkey)
    except AssertionError:
        raise ValueError("Invalid argument") from None

    accounts = MultisigSetConfigAuthorityAccounts(
        multisig=multisig_pda,
        config_authority=config_authority,
        rent_payer=None,
    )

    args = MultisigSetConfigAuthorityArgs(
        args=MultisigSetConfigAuthorityArgsType(
            memo=memo,
            config_authority=new_config_authority,
        )
    )

    return multisig_set_config_authority_instruction(
        accounts=accounts, args=args, program_id=program_id
    )
