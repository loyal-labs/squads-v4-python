from solders.keypair import Keypair
from solders.null_signer import NullSigner
from solders.presigner import Presigner

SignerList = list[Keypair | Presigner | NullSigner]
