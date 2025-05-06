from solders.pubkey import Pubkey

from generated.instructions.batch_create import batch_create as batch_create_instruction
from generated.program_id import PROGRAM_ID


# def batch_create(
#     multisig_pda: Pubkey,
#     creator: Pubkey,
#     rent_payer: Pubkey,
#     batch_index: int,
#     vault_index: int,
# ):
#     batch_pda = get_transaction_pda(multisig_pda, batch_index)
