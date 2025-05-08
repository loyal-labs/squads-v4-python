from solders.instruction import Instruction
from solders.pubkey import Pubkey

from src.generated.instructions.multisig_create_v2 import (
    MultisigCreateV2Accounts,
    MultisigCreateV2Args,
)
from src.generated.instructions.multisig_create_v2 import (
    multisig_create_v2 as multisig_create_v2_instruction,
)
from src.generated.types.member import Member
from src.generated.types.multisig_create_args_v2 import MultisigCreateArgsV2
from src.pda import get_program_config_pda


def multisig_create_v2(
    treasury: Pubkey,
    creator: Pubkey,
    multisig: Pubkey,
    config_authority: Pubkey | None,
    threshold: int,
    members: list[Member],
    time_lock: int,
    create_key: Pubkey,
    rent_collector: Pubkey | None,
    memo: str | None,
    program_id: Pubkey,
) -> Instruction:
    try:
        assert isinstance(treasury, Pubkey)
        assert isinstance(creator, Pubkey)
        assert isinstance(multisig, Pubkey)
        assert isinstance(config_authority, Pubkey) or config_authority is None
        assert isinstance(threshold, int)
        assert isinstance(members, list)
        assert isinstance(time_lock, int)
        assert isinstance(create_key, Pubkey)
        assert isinstance(rent_collector, Pubkey) or rent_collector is None
        assert isinstance(memo, str | None)
        assert isinstance(program_id, Pubkey)
    except AssertionError:
        raise ValueError("Invalid argument") from None

    program_config_tuple = get_program_config_pda(program_id)
    program_config_pda = program_config_tuple[0]

    accounts = MultisigCreateV2Accounts(
        program_config=program_config_pda,
        treasury=treasury,
        multisig=multisig,
        create_key=create_key,
        creator=creator,
    )

    args = MultisigCreateV2Args(
        args=MultisigCreateArgsV2(
            config_authority=config_authority,
            threshold=threshold,
            members=members,
            time_lock=time_lock,
            rent_collector=rent_collector,
            memo=memo,
        )
    )
    return multisig_create_v2_instruction(args, accounts, program_id)
