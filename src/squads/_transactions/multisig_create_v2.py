from solders.hash import Hash
from solders.message import MessageV0
from solders.pubkey import Pubkey
from solders.transaction import Signer, VersionedTransaction

from ..generated.types.member import Member
from ..instructions import multisig_create_v2 as create_instruction


def multisig_create_v2(
    blockhash: Hash,
    treasury: Pubkey,
    create_key: Signer,
    creator: Signer,
    multisig_pda: Pubkey,
    config_authority: Pubkey | None,
    threshold: int,
    members: list[Member],
    time_lock: int,
    rent_collector: Pubkey | None,
    memo: str | None,
    program_id: Pubkey,
) -> VersionedTransaction:
    """
    Creates a new multisig account.
    """
    assert isinstance(treasury, Pubkey), "Invalid treasury"
    assert isinstance(create_key, Signer), "Invalid create_key"
    assert isinstance(creator, Signer), "Invalid creator"
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

    instruction = create_instruction(
        treasury,
        creator.pubkey(),
        multisig_pda,
        config_authority,
        threshold,
        members,
        time_lock,
        create_key.pubkey(),
        rent_collector,
        memo,
        program_id,
    )

    try:
        message_v0 = MessageV0.try_compile(
            creator.pubkey(),
            [instruction],
            [],
            blockhash,
        )
    except Exception as e:
        raise e from None

    try:
        versioned_tx = VersionedTransaction(message_v0, [creator, create_key])
        return versioned_tx
    except Exception as e:
        raise e from None
