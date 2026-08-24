from pathlib import Path
import secrets
import json
import base64

import oqs

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.x25519 import (
    X25519PrivateKey
)
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


# ==========================================
# CONFIGURATION
# ==========================================

INPUT_FILE = Path("input/sample.txt")
OUTPUT_DIR = Path("output")

ENCRYPTED_FILE = OUTPUT_DIR / "sample.enc"
METADATA_FILE = OUTPUT_DIR / "metadata.json"

OUTPUT_DIR.mkdir(exist_ok=True)


# ==========================================
# 1. RECEIVER X25519 KEY PAIR
# ==========================================

receiver_x25519_private = X25519PrivateKey.generate()
receiver_x25519_public = receiver_x25519_private.public_key()

print("Receiver X25519 key pair generated.")


# ==========================================
# 2. SENDER EPHEMERAL X25519 KEY PAIR
# ==========================================

sender_x25519_private = X25519PrivateKey.generate()
sender_x25519_public = sender_x25519_private.public_key()

print("Sender X25519 ephemeral key pair generated.")


# ==========================================
# 3. X25519 SHARED SECRET
# ==========================================

x25519_secret = sender_x25519_private.exchange(
    receiver_x25519_public
)

print("X25519 shared secret generated.")


# ==========================================
# 4. RECEIVER ML-KEM-768 KEY PAIR
# ==========================================

kem = oqs.KeyEncapsulation("ML-KEM-768")

receiver_mlkem_public = kem.generate_keypair()
receiver_mlkem_private = kem.export_secret_key()

print("Receiver ML-KEM-768 key pair generated.")


# ==========================================
# 5. ML-KEM ENCAPSULATION
# ==========================================

mlkem_ciphertext, mlkem_secret = kem.encap_secret(
    receiver_mlkem_public
)

print("ML-KEM-768 encapsulation successful.")


# ==========================================
# 6. COMBINE HYBRID SECRETS
# ==========================================

combined_secret = (
    x25519_secret +
    mlkem_secret
)


# ==========================================
# 7. HKDF → AES-256 KEY
# ==========================================

hkdf = HKDF(
    algorithm=hashes.SHA256(),
    length=32,
    salt=None,
    info=b"HybridCrypto-AES-Key"
)

aes_key = hkdf.derive(combined_secret)

print("Hybrid AES-256 key derived.")


# ==========================================
# 8. READ INPUT FILE
# ==========================================

plaintext = INPUT_FILE.read_bytes()

print(f"Input file size: {len(plaintext)} bytes")


# ==========================================
# 9. AES-256-GCM ENCRYPTION
# ==========================================

aes = AESGCM(aes_key)

nonce = secrets.token_bytes(12)

encrypted_data = aes.encrypt(
    nonce,
    plaintext,
    None
)

ENCRYPTED_FILE.write_bytes(encrypted_data)

print("File encrypted successfully.")
print(f"Encrypted file: {ENCRYPTED_FILE}")


# ==========================================
# 10. SAVE PUBLIC/NON-SECRET METADATA
# ==========================================

metadata = {
    "algorithm": "Hybrid X25519 + ML-KEM-768 + HKDF-SHA256 + AES-256-GCM",

    "x25519_sender_public_key":
        base64.b64encode(
            sender_x25519_public.public_bytes_raw()
        ).decode(),

    "mlkem_ciphertext":
        base64.b64encode(
            mlkem_ciphertext
        ).decode(),

    "nonce":
        base64.b64encode(
            nonce
        ).decode()
}

METADATA_FILE.write_text(
    json.dumps(metadata, indent=4)
)

print("Public encryption metadata saved.")
print(f"Metadata: {METADATA_FILE}")


# ==========================================
# 11. SAVE PRIVATE KEYS LOCALLY
# ==========================================
#
# NOTE:
# These are ONLY for our local prototype.
# In the final cloud system, these private keys
# must be protected by the KMS.
#

private_key_data = {
    "x25519_receiver_private_key":
        base64.b64encode(
            receiver_x25519_private.private_bytes_raw()
        ).decode(),

    "mlkem_receiver_private_key":
        base64.b64encode(
            receiver_mlkem_private
        ).decode()
}

PRIVATE_KEY_FILE = OUTPUT_DIR / "private_keys.json"

PRIVATE_KEY_FILE.write_text(
    json.dumps(private_key_data, indent=4)
)

print("Private keys saved locally for prototype testing.")
print("IMPORTANT: Private keys must NOT be uploaded to GitHub.")