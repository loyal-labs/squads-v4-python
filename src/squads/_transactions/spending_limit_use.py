from solders.hash import Hash
from solders.message import MessageV0
from solders.pubkey import Pubkey
from solders.transaction import Signer, VersionedTransaction

from ..instructions import spending_limit_use as create_instruction


def spending_limit_use(
    blockhash: Hash,
    fee_payer: Signer,
    multisig_pda: Pubkey,
    member: Signer,
    spending_limit: Pubkey,
    mint: Pubkey | None,
    vault_index: int,
    amount: int,
    decimals: int,
    destination: Pubkey,
    token_program: Pubkey | None,
    memo: str | None,
    program_id: Pubkey,
) -> VersionedTransaction:
    """
    Returns unsigned `VersionedTransaction` that needs to be
    signed by `member` and `feePayer` before sending it.
    """
    assert isinstance(fee_payer, Signer)
    assert isinstance(multisig_pda, Pubkey)
    assert isinstance(member, Signer)
    assert isinstance(spending_limit, Pubkey)
    assert isinstance(mint, Pubkey) or mint is None
    assert isinstance(vault_index, int)
    assert isinstance(amount, int)
    assert isinstance(decimals, int)
    assert isinstance(destination, Pubkey)
    assert isinstance(token_program, Pubkey) or token_program is None
    assert isinstance(memo, str) or memo is None
    assert isinstance(program_id, Pubkey)

    ix = create_instruction(
        multisig_pda,
        member.pubkey(),
        spending_limit,
        mint,
        vault_index,
        amount,
        decimals,
        destination,
        token_program,
        memo,
        program_id,
    )
    message_v0 = MessageV0.try_compile(
        fee_payer.pubkey(),
        [ix],
        [],
        blockhash,
    )
    signers_list = [fee_payer, member]
    # unique signers
    signers = list(set(signers_list))

    versioned_tx = VersionedTransaction(message_v0, signers)

    return versioned_tx
