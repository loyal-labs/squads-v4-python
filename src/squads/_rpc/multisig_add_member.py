from collections.abc import Sequence

from solana.rpc.async_api import AsyncClient
from solana.rpc.types import TxOpts
from solders.pubkey import Pubkey
from solders.rpc.responses import SendTransactionResp
from solders.transaction import Signer

from .._internal.utils import get_recent_blockhash
from ..generated.program_id import PROGRAM_ID
from ..generated.types.member import Member
from ..transactions import multisig_add_member as create_transaction


async def multisig_add_member(
    connection: AsyncClient,
    fee_payer: Signer,
    multisig_pda: Pubkey,
    config_authority: Pubkey,
    rent_payer: Signer,
    new_member: Member,
    memo: str | None = None,
    signers: Sequence[Signer] | None = None,
    send_options: TxOpts | None = None,
    program_id: Pubkey | None = PROGRAM_ID,
) -> SendTransactionResp:
    """Add a member/key to the multisig and reallocate space if necessary.

    Must be signed by fee_payer, rent_payer and signers
    """
    assert isinstance(connection, AsyncClient)
    assert isinstance(fee_payer, Signer)
    assert isinstance(multisig_pda, Pubkey)
    assert isinstance(config_authority, Pubkey)
    assert isinstance(rent_payer, Signer)
    assert isinstance(new_member, Member)
    assert isinstance(memo, str) or memo is None
    assert isinstance(signers, Sequence) or signers is None
    assert isinstance(send_options, TxOpts) or send_options is None
    assert isinstance(program_id, Pubkey) or program_id is None

    tx = create_transaction(
        await get_recent_blockhash(connection),
        fee_payer,
        multisig_pda,
        config_authority,
        rent_payer,
        new_member,
        memo,
        program_id,
    )

    try:
        return await connection.send_transaction(tx, send_options)
    except Exception as e:
        raise e from None
