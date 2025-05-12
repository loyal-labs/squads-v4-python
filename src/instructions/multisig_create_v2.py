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
from src.pda import PDA


def multisig_create_v2(
    treasury: Pubkey,
    creator: Pubkey,
    multisig_pda: Pubkey,
    config_authority: Pubkey | None,
    threshold: int,
    members: list[Member],
    time_lock: int,
    create_key: Pubkey,
    rent_collector: Pubkey | None,
    memo: str | None,
    program_id: Pubkey,
) -> Instruction:
    assert isinstance(treasury, Pubkey), "Invalid treasury"
    assert isinstance(create_key, Pubkey), "Invalid create_key"
    assert isinstance(creator, Pubkey), "Invalid creator"
    assert isinstance(multisig_pda, Pubkey), "Invalid multisig_pda"
    assert isinstance(config_authority, Pubkey | None), "Invalid config_authority"
    assert isinstance(threshold, int), "Invalid threshold"
    assert isinstance(members, list), "Invalid members"
    assert len(members) > 0, "Invalid members (must be non-empty)"
    assert isinstance(time_lock, int), "Invalid time_lock"
    assert time_lock >= 0, "Invalid time_lock (must be >= 0)"
    assert isinstance(rent_collector, Pubkey | None), "Invalid rent_collector"
    assert isinstance(memo, str | None), "Invalid memo"
    assert isinstance(program_id, Pubkey), "Invalid program_id"

    program_config_tuple = PDA.get_program_config_pda(program_id)
    program_config_pda = program_config_tuple[0]

    accounts = MultisigCreateV2Accounts(
        program_config=program_config_pda,
        treasury=treasury,
        multisig=multisig_pda,
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
