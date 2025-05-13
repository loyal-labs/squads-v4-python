from collections.abc import Sequence

from solders.hash import Hash
from solders.message import MessageV0
from solders.pubkey import Pubkey
from solders.transaction import Signer, VersionedTransaction

from ..generated.types.member import Member
from ..instructions import multisig_add_member as create_instruction


def multisig_add_member(
    blockhash: Hash,
    fee_payer: Signer,
    multisig_pda: Pubkey,
    config_authority: Pubkey,
    rent_payer: Signer,
    new_member: Member,
    memo: str | None = None,
    program_id: Pubkey | None = None,
    signers: Sequence[Signer] | None = None,
) -> VersionedTransaction:
    """Add a member/key to the multisig and reallocate space if necessary."""
    assert isinstance(fee_payer, Signer)
    assert isinstance(multisig_pda, Pubkey)
    assert isinstance(config_authority, Pubkey)
    assert isinstance(rent_payer, Signer)
    assert isinstance(new_member, Member)
    assert isinstance(memo, str) or memo is None
    assert isinstance(program_id, Pubkey) or program_id is None

    ix = create_instruction(
        multisig_pda,
        config_authority,
        rent_payer.pubkey(),
        new_member,
        memo,
        program_id,
    )
    message_v0 = MessageV0.try_compile(
        fee_payer.pubkey(),
        [ix],
        [],
        blockhash,
    )

    signers_array = [fee_payer, rent_payer]
    if signers is not None:
        signers_array.extend(signers)

    # only unique signers
    signers_array = list(set(signers_array))

    versioned_tx = VersionedTransaction(message_v0, signers_array)

    return versioned_tx
