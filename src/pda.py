from solders.pubkey import Pubkey

from src._internal.nums import to_u8_bytes, to_u32_bytes, to_u64_bytes, to_utf_bytes
from src.generated.program_id import PROGRAM_ID

SEED_PREFIX = to_utf_bytes("multisig")
SEED_PROGRAM_CONFIG = to_utf_bytes("program_config")
SEED_MULTISIG = to_utf_bytes("multisig")
SEED_VAULT = to_utf_bytes("vault")
SEED_TRANSACTION = to_utf_bytes("transaction")
SEED_PROPOSAL = to_utf_bytes("proposal")
SEED_BATCH_TRANSACTION = to_utf_bytes("batch_transaction")
SEED_EPHEMERAL_SIGNER = to_utf_bytes("ephemeral_signer")
SEED_SPENDING_LIMIT = to_utf_bytes("spending_limit")


class PDA:
    @staticmethod
    def get_program_config_pda(program_id: Pubkey = PROGRAM_ID) -> tuple[Pubkey, int]:
        return Pubkey.find_program_address(
            [SEED_PREFIX, SEED_PROGRAM_CONFIG], program_id
        )

    @staticmethod
    def get_multisig_pda(
        create_key: Pubkey, program_id: Pubkey = PROGRAM_ID
    ) -> tuple[Pubkey, int]:
        create_key_bytes = create_key.__bytes__()
        return Pubkey.find_program_address(
            [SEED_PREFIX, SEED_MULTISIG, create_key_bytes], program_id
        )

    @staticmethod
    def get_vault_pda(
        multisig_pda: Pubkey, index: int, program_id: Pubkey = PROGRAM_ID
    ) -> tuple[Pubkey, int]:
        assert 0 <= index < 256, "Invalid vault index"

        multisig_pda_bytes = multisig_pda.__bytes__()
        return Pubkey.find_program_address(
            [SEED_PREFIX, multisig_pda_bytes, SEED_VAULT, to_u8_bytes(index)],
            program_id,
        )

    @staticmethod
    def get_ephemeral_signer_pda(
        transaction_pda: Pubkey, ephemeral_signer_index: int, program_id: Pubkey | None
    ) -> tuple[Pubkey, int]:
        transaction_pda_bytes = transaction_pda.__bytes__()

        if program_id is None:
            program_id = PROGRAM_ID

        return Pubkey.find_program_address(
            [
                SEED_PREFIX,
                transaction_pda_bytes,
                SEED_EPHEMERAL_SIGNER,
                to_u8_bytes(ephemeral_signer_index),
            ],
            program_id,
        )

    @staticmethod
    def get_transaction_pda(
        multisig_pda: Pubkey, index: int, program_id: Pubkey = PROGRAM_ID
    ) -> tuple[Pubkey, int]:
        multisig_pda_bytes = multisig_pda.__bytes__()

        return Pubkey.find_program_address(
            [SEED_PREFIX, multisig_pda_bytes, SEED_TRANSACTION, to_u64_bytes(index)],
            program_id,
        )

    @staticmethod
    def get_proposal_pda(
        multisig_pda: Pubkey, transaction_index: int, program_id: Pubkey = PROGRAM_ID
    ) -> tuple[Pubkey, int]:
        multisig_pda_bytes = multisig_pda.__bytes__()

        return Pubkey.find_program_address(
            [
                SEED_PREFIX,
                multisig_pda_bytes,
                SEED_TRANSACTION,
                to_u64_bytes(transaction_index),
                SEED_PROPOSAL,
            ],
            program_id,
        )

    @staticmethod
    def get_batch_transaction_pda(
        multisig_pda: Pubkey,
        batch_index: int,
        transaction_index: int,
        program_id: Pubkey = PROGRAM_ID,
    ) -> tuple[Pubkey, int]:
        multisig_pda_bytes = multisig_pda.__bytes__()

        return Pubkey.find_program_address(
            [
                SEED_PREFIX,
                multisig_pda_bytes,
                SEED_TRANSACTION,
                to_u64_bytes(batch_index),
                SEED_BATCH_TRANSACTION,
                to_u32_bytes(transaction_index),
            ],
            program_id,
        )

    @staticmethod
    def get_spending_limit_pda(
        multisig_pda: Pubkey, create_key: Pubkey, program_id: Pubkey = PROGRAM_ID
    ) -> tuple[Pubkey, int]:
        multisig_pda_bytes = multisig_pda.__bytes__()
        create_key_bytes = create_key.__bytes__()

        return Pubkey.find_program_address(
            [SEED_PREFIX, multisig_pda_bytes, SEED_SPENDING_LIMIT, create_key_bytes],
            program_id,
        )
