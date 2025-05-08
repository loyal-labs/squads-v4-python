from solders.hash import Hash
from solders.message import MessageV0
from solders.pubkey import Pubkey
from solders.signature import Signature
from solders.transaction import VersionedTransaction

from src.generated.types.member import Member
from src.instructions.multisig_add_member import (
    multisig_add_member as create_instruction,
)


def multisig_add_member(
    blockhash: Hash,
    fee_payer: Pubkey,
    multisig_pda: Pubkey,
    config_authority: Pubkey,
    rent_payer: Pubkey,
    new_member: Member,
    memo: str | None,
    program_id: Pubkey | None,
) -> VersionedTransaction:
    """
    Returns unsigned `VersionedTransaction` that needs to be
    signed by `configAuthority` and `feePayer` before sending it.
    """
    try:
        assert isinstance(blockhash, Hash)
        assert isinstance(fee_payer, Pubkey)
        assert isinstance(multisig_pda, Pubkey)
        assert isinstance(config_authority, Pubkey)
        assert isinstance(rent_payer, Pubkey)
        assert isinstance(new_member, Member)
        assert isinstance(memo, str) or memo is None
        assert isinstance(program_id, Pubkey) or program_id is None
    except AssertionError:
        raise ValueError("Invalid argument") from None

    ix = create_instruction(
        multisig_pda,
        config_authority,
        rent_payer,
        new_member,
        memo,
        program_id,
    )
    message_v0 = MessageV0.try_compile(
        fee_payer,
        [ix],
        [],
        blockhash,
    )
    num_signers = message_v0.header.num_required_signatures
    signers = [Signature.default() for _ in range(num_signers)]

    versioned_tx = VersionedTransaction.populate(message_v0, signers)

    return versioned_tx
