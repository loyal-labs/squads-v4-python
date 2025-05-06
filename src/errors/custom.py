import typing
from anchorpy.error import ProgramError


class DuplicateMember(ProgramError):
    def __init__(self) -> None:
        super().__init__(6000, "Found multiple members with the same pubkey")

    code = 6000
    name = "DuplicateMember"
    msg = "Found multiple members with the same pubkey"


class EmptyMembers(ProgramError):
    def __init__(self) -> None:
        super().__init__(6001, "Members array is empty")

    code = 6001
    name = "EmptyMembers"
    msg = "Members array is empty"


class TooManyMembers(ProgramError):
    def __init__(self) -> None:
        super().__init__(6002, "Too many members, can be up to 65535")

    code = 6002
    name = "TooManyMembers"
    msg = "Too many members, can be up to 65535"


class InvalidThreshold(ProgramError):
    def __init__(self) -> None:
        super().__init__(
            6003,
            "Invalid threshold, must be between 1 and number of members with Vote permission",
        )

    code = 6003
    name = "InvalidThreshold"
    msg = "Invalid threshold, must be between 1 and number of members with Vote permission"


class Unauthorized(ProgramError):
    def __init__(self) -> None:
        super().__init__(6004, "Attempted to perform an unauthorized action")

    code = 6004
    name = "Unauthorized"
    msg = "Attempted to perform an unauthorized action"


class NotAMember(ProgramError):
    def __init__(self) -> None:
        super().__init__(6005, "Provided pubkey is not a member of multisig")

    code = 6005
    name = "NotAMember"
    msg = "Provided pubkey is not a member of multisig"


class InvalidTransactionMessage(ProgramError):
    def __init__(self) -> None:
        super().__init__(6006, "TransactionMessage is malformed.")

    code = 6006
    name = "InvalidTransactionMessage"
    msg = "TransactionMessage is malformed."


class StaleProposal(ProgramError):
    def __init__(self) -> None:
        super().__init__(6007, "Proposal is stale")

    code = 6007
    name = "StaleProposal"
    msg = "Proposal is stale"


class InvalidProposalStatus(ProgramError):
    def __init__(self) -> None:
        super().__init__(6008, "Invalid proposal status")

    code = 6008
    name = "InvalidProposalStatus"
    msg = "Invalid proposal status"


class InvalidTransactionIndex(ProgramError):
    def __init__(self) -> None:
        super().__init__(6009, "Invalid transaction index")

    code = 6009
    name = "InvalidTransactionIndex"
    msg = "Invalid transaction index"


class AlreadyApproved(ProgramError):
    def __init__(self) -> None:
        super().__init__(6010, "Member already approved the transaction")

    code = 6010
    name = "AlreadyApproved"
    msg = "Member already approved the transaction"


class AlreadyRejected(ProgramError):
    def __init__(self) -> None:
        super().__init__(6011, "Member already rejected the transaction")

    code = 6011
    name = "AlreadyRejected"
    msg = "Member already rejected the transaction"


class AlreadyCancelled(ProgramError):
    def __init__(self) -> None:
        super().__init__(6012, "Member already cancelled the transaction")

    code = 6012
    name = "AlreadyCancelled"
    msg = "Member already cancelled the transaction"


class InvalidNumberOfAccounts(ProgramError):
    def __init__(self) -> None:
        super().__init__(6013, "Wrong number of accounts provided")

    code = 6013
    name = "InvalidNumberOfAccounts"
    msg = "Wrong number of accounts provided"


class InvalidAccount(ProgramError):
    def __init__(self) -> None:
        super().__init__(6014, "Invalid account provided")

    code = 6014
    name = "InvalidAccount"
    msg = "Invalid account provided"


class RemoveLastMember(ProgramError):
    def __init__(self) -> None:
        super().__init__(6015, "Cannot remove last member")

    code = 6015
    name = "RemoveLastMember"
    msg = "Cannot remove last member"


class NoVoters(ProgramError):
    def __init__(self) -> None:
        super().__init__(6016, "Members don't include any voters")

    code = 6016
    name = "NoVoters"
    msg = "Members don't include any voters"


class NoProposers(ProgramError):
    def __init__(self) -> None:
        super().__init__(6017, "Members don't include any proposers")

    code = 6017
    name = "NoProposers"
    msg = "Members don't include any proposers"


class NoExecutors(ProgramError):
    def __init__(self) -> None:
        super().__init__(6018, "Members don't include any executors")

    code = 6018
    name = "NoExecutors"
    msg = "Members don't include any executors"


class InvalidStaleTransactionIndex(ProgramError):
    def __init__(self) -> None:
        super().__init__(
            6019, "`stale_transaction_index` must be <= `transaction_index`"
        )

    code = 6019
    name = "InvalidStaleTransactionIndex"
    msg = "`stale_transaction_index` must be <= `transaction_index`"


class NotSupportedForControlled(ProgramError):
    def __init__(self) -> None:
        super().__init__(6020, "Instruction not supported for controlled multisig")

    code = 6020
    name = "NotSupportedForControlled"
    msg = "Instruction not supported for controlled multisig"


class TimeLockNotReleased(ProgramError):
    def __init__(self) -> None:
        super().__init__(6021, "Proposal time lock has not been released")

    code = 6021
    name = "TimeLockNotReleased"
    msg = "Proposal time lock has not been released"


class NoActions(ProgramError):
    def __init__(self) -> None:
        super().__init__(6022, "Config transaction must have at least one action")

    code = 6022
    name = "NoActions"
    msg = "Config transaction must have at least one action"


class MissingAccount(ProgramError):
    def __init__(self) -> None:
        super().__init__(6023, "Missing account")

    code = 6023
    name = "MissingAccount"
    msg = "Missing account"


class InvalidMint(ProgramError):
    def __init__(self) -> None:
        super().__init__(6024, "Invalid mint")

    code = 6024
    name = "InvalidMint"
    msg = "Invalid mint"


class InvalidDestination(ProgramError):
    def __init__(self) -> None:
        super().__init__(6025, "Invalid destination")

    code = 6025
    name = "InvalidDestination"
    msg = "Invalid destination"


class SpendingLimitExceeded(ProgramError):
    def __init__(self) -> None:
        super().__init__(6026, "Spending limit exceeded")

    code = 6026
    name = "SpendingLimitExceeded"
    msg = "Spending limit exceeded"


class DecimalsMismatch(ProgramError):
    def __init__(self) -> None:
        super().__init__(6027, "Decimals don't match the mint")

    code = 6027
    name = "DecimalsMismatch"
    msg = "Decimals don't match the mint"


class UnknownPermission(ProgramError):
    def __init__(self) -> None:
        super().__init__(6028, "Member has unknown permission")

    code = 6028
    name = "UnknownPermission"
    msg = "Member has unknown permission"


class ProtectedAccount(ProgramError):
    def __init__(self) -> None:
        super().__init__(
            6029, "Account is protected, it cannot be passed into a CPI as writable"
        )

    code = 6029
    name = "ProtectedAccount"
    msg = "Account is protected, it cannot be passed into a CPI as writable"


class TimeLockExceedsMaxAllowed(ProgramError):
    def __init__(self) -> None:
        super().__init__(6030, "Time lock exceeds the maximum allowed (90 days)")

    code = 6030
    name = "TimeLockExceedsMaxAllowed"
    msg = "Time lock exceeds the maximum allowed (90 days)"


class IllegalAccountOwner(ProgramError):
    def __init__(self) -> None:
        super().__init__(6031, "Account is not owned by Multisig program")

    code = 6031
    name = "IllegalAccountOwner"
    msg = "Account is not owned by Multisig program"


class RentReclamationDisabled(ProgramError):
    def __init__(self) -> None:
        super().__init__(6032, "Rent reclamation is disabled for this multisig")

    code = 6032
    name = "RentReclamationDisabled"
    msg = "Rent reclamation is disabled for this multisig"


class InvalidRentCollector(ProgramError):
    def __init__(self) -> None:
        super().__init__(6033, "Invalid rent collector address")

    code = 6033
    name = "InvalidRentCollector"
    msg = "Invalid rent collector address"


class ProposalForAnotherMultisig(ProgramError):
    def __init__(self) -> None:
        super().__init__(6034, "Proposal is for another multisig")

    code = 6034
    name = "ProposalForAnotherMultisig"
    msg = "Proposal is for another multisig"


class TransactionForAnotherMultisig(ProgramError):
    def __init__(self) -> None:
        super().__init__(6035, "Transaction is for another multisig")

    code = 6035
    name = "TransactionForAnotherMultisig"
    msg = "Transaction is for another multisig"


class TransactionNotMatchingProposal(ProgramError):
    def __init__(self) -> None:
        super().__init__(6036, "Transaction doesn't match proposal")

    code = 6036
    name = "TransactionNotMatchingProposal"
    msg = "Transaction doesn't match proposal"


class TransactionNotLastInBatch(ProgramError):
    def __init__(self) -> None:
        super().__init__(6037, "Transaction is not last in batch")

    code = 6037
    name = "TransactionNotLastInBatch"
    msg = "Transaction is not last in batch"


class BatchNotEmpty(ProgramError):
    def __init__(self) -> None:
        super().__init__(6038, "Batch is not empty")

    code = 6038
    name = "BatchNotEmpty"
    msg = "Batch is not empty"


class SpendingLimitInvalidAmount(ProgramError):
    def __init__(self) -> None:
        super().__init__(6039, "Invalid SpendingLimit amount")

    code = 6039
    name = "SpendingLimitInvalidAmount"
    msg = "Invalid SpendingLimit amount"


class InvalidInstructionArgs(ProgramError):
    def __init__(self) -> None:
        super().__init__(6040, "Invalid Instruction Arguments")

    code = 6040
    name = "InvalidInstructionArgs"
    msg = "Invalid Instruction Arguments"


class FinalBufferHashMismatch(ProgramError):
    def __init__(self) -> None:
        super().__init__(
            6041, "Final message buffer hash doesnt match the expected hash"
        )

    code = 6041
    name = "FinalBufferHashMismatch"
    msg = "Final message buffer hash doesnt match the expected hash"


class FinalBufferSizeExceeded(ProgramError):
    def __init__(self) -> None:
        super().__init__(6042, "Final buffer size cannot exceed 4000 bytes")

    code = 6042
    name = "FinalBufferSizeExceeded"
    msg = "Final buffer size cannot exceed 4000 bytes"


class FinalBufferSizeMismatch(ProgramError):
    def __init__(self) -> None:
        super().__init__(6043, "Final buffer size mismatch")

    code = 6043
    name = "FinalBufferSizeMismatch"
    msg = "Final buffer size mismatch"


class MultisigCreateDeprecated(ProgramError):
    def __init__(self) -> None:
        super().__init__(
            6044, "multisig_create has been deprecated. Use multisig_create_v2 instead."
        )

    code = 6044
    name = "MultisigCreateDeprecated"
    msg = "multisig_create has been deprecated. Use multisig_create_v2 instead."


CustomError = typing.Union[
    DuplicateMember,
    EmptyMembers,
    TooManyMembers,
    InvalidThreshold,
    Unauthorized,
    NotAMember,
    InvalidTransactionMessage,
    StaleProposal,
    InvalidProposalStatus,
    InvalidTransactionIndex,
    AlreadyApproved,
    AlreadyRejected,
    AlreadyCancelled,
    InvalidNumberOfAccounts,
    InvalidAccount,
    RemoveLastMember,
    NoVoters,
    NoProposers,
    NoExecutors,
    InvalidStaleTransactionIndex,
    NotSupportedForControlled,
    TimeLockNotReleased,
    NoActions,
    MissingAccount,
    InvalidMint,
    InvalidDestination,
    SpendingLimitExceeded,
    DecimalsMismatch,
    UnknownPermission,
    ProtectedAccount,
    TimeLockExceedsMaxAllowed,
    IllegalAccountOwner,
    RentReclamationDisabled,
    InvalidRentCollector,
    ProposalForAnotherMultisig,
    TransactionForAnotherMultisig,
    TransactionNotMatchingProposal,
    TransactionNotLastInBatch,
    BatchNotEmpty,
    SpendingLimitInvalidAmount,
    InvalidInstructionArgs,
    FinalBufferHashMismatch,
    FinalBufferSizeExceeded,
    FinalBufferSizeMismatch,
    MultisigCreateDeprecated,
]
CUSTOM_ERROR_MAP: dict[int, CustomError] = {
    6000: DuplicateMember(),
    6001: EmptyMembers(),
    6002: TooManyMembers(),
    6003: InvalidThreshold(),
    6004: Unauthorized(),
    6005: NotAMember(),
    6006: InvalidTransactionMessage(),
    6007: StaleProposal(),
    6008: InvalidProposalStatus(),
    6009: InvalidTransactionIndex(),
    6010: AlreadyApproved(),
    6011: AlreadyRejected(),
    6012: AlreadyCancelled(),
    6013: InvalidNumberOfAccounts(),
    6014: InvalidAccount(),
    6015: RemoveLastMember(),
    6016: NoVoters(),
    6017: NoProposers(),
    6018: NoExecutors(),
    6019: InvalidStaleTransactionIndex(),
    6020: NotSupportedForControlled(),
    6021: TimeLockNotReleased(),
    6022: NoActions(),
    6023: MissingAccount(),
    6024: InvalidMint(),
    6025: InvalidDestination(),
    6026: SpendingLimitExceeded(),
    6027: DecimalsMismatch(),
    6028: UnknownPermission(),
    6029: ProtectedAccount(),
    6030: TimeLockExceedsMaxAllowed(),
    6031: IllegalAccountOwner(),
    6032: RentReclamationDisabled(),
    6033: InvalidRentCollector(),
    6034: ProposalForAnotherMultisig(),
    6035: TransactionForAnotherMultisig(),
    6036: TransactionNotMatchingProposal(),
    6037: TransactionNotLastInBatch(),
    6038: BatchNotEmpty(),
    6039: SpendingLimitInvalidAmount(),
    6040: InvalidInstructionArgs(),
    6041: FinalBufferHashMismatch(),
    6042: FinalBufferSizeExceeded(),
    6043: FinalBufferSizeMismatch(),
    6044: MultisigCreateDeprecated(),
}


def from_code(code: int) -> typing.Optional[CustomError]:
    maybe_err = CUSTOM_ERROR_MAP.get(code)
    if maybe_err is None:
        return None
    return maybe_err
