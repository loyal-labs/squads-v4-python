from solders.hash import Hash
from solders.message import MessageV0
from solders.pubkey import Pubkey
from solders.signature import Signature
from solders.transaction import VersionedTransaction

from src.generated.types.member import Member
from src.instructions.multisig_create_v2 import multisig_create_v2 as create_instruction


def multisig_create_v2(
    blockhash: Hash,
    treasury: Pubkey,
    create_key: Pubkey,
    creator: Pubkey,
    multisig: Pubkey,
    config_authority: Pubkey | None,
    threshold: int,
    members: list[Member],
    time_lock: int,
    rent_collector: Pubkey | None,
    memo: str | None,
    program_id: Pubkey,
) -> VersionedTransaction:
    """
    Returns unsigned `VersionedTransaction` that needs to be
    signed by `creator` and `create_key` before sending it.
    """
    try:
        assert isinstance(blockhash, Hash)
        assert isinstance(treasury, Pubkey)
        assert isinstance(create_key, Pubkey)
        assert isinstance(creator, Pubkey)
        assert isinstance(multisig, Pubkey)
        assert isinstance(config_authority, Pubkey | None)
        assert isinstance(threshold, int)
        assert isinstance(members, list)
        assert isinstance(time_lock, int)
        assert isinstance(rent_collector, Pubkey | None)
        assert isinstance(memo, str | None)
        assert isinstance(program_id, Pubkey)
    except AssertionError:
        raise ValueError("Invalid argument") from None

    instruction = create_instruction(
        treasury,
        creator,
        multisig,
        config_authority,
        threshold,
        members,
        time_lock,
        create_key,
        rent_collector,
        memo,
        program_id,
    )

    message_v0 = MessageV0.try_compile(
        creator,
        [instruction],
        [],
        blockhash,
    )

    num_signers = message_v0.header.num_required_signatures
    signers = [Signature.default() for _ in range(num_signers)]

    versioned_tx = VersionedTransaction.populate(message_v0, signers)

    return versioned_tx
