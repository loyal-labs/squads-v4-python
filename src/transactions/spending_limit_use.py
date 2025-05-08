from solders.hash import Hash
from solders.message import MessageV0
from solders.pubkey import Pubkey
from solders.signature import Signature
from solders.transaction import VersionedTransaction

from src.instructions.spending_limit_use import spending_limit_use as create_instruction


def spending_limit_use(
    blockhash: Hash,
    fee_payer: Pubkey,
    multisig_pda: Pubkey,
    member: Pubkey,
    spending_limit: Pubkey,
    mint: Pubkey,
    vault_index: int,
    amount: int,
    decimals: int,
    destination: Pubkey,
    token_program: Pubkey,
    memo: str | None,
    program_id: Pubkey | None,
) -> VersionedTransaction:
    """
    Returns unsigned `VersionedTransaction` that needs to be
    signed by `member` and `feePayer` before sending it.
    """
    try:
        assert isinstance(fee_payer, Pubkey)
        assert isinstance(multisig_pda, Pubkey)
        assert isinstance(member, Pubkey)
        assert isinstance(spending_limit, Pubkey)
        assert isinstance(mint, Pubkey)
        assert isinstance(vault_index, int)
        assert isinstance(amount, int)
        assert isinstance(decimals, int)
        assert isinstance(destination, Pubkey)
        assert isinstance(token_program, Pubkey)
        assert isinstance(memo, str) or memo is None
        assert isinstance(program_id, Pubkey) or program_id is None
    except AssertionError:
        raise ValueError("Invalid argument") from None

    ix = create_instruction(
        multisig_pda,
        member,
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
        fee_payer,
        [ix],
        [],
        blockhash,
    )
    num_signers = message_v0.header.num_required_signatures
    signers = [Signature.default() for _ in range(num_signers)]

    versioned_tx = VersionedTransaction.populate(message_v0, signers)

    return versioned_tx
