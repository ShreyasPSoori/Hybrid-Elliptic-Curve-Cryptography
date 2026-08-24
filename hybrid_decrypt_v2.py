from pathlib import Path
import json
import base64

import oqs

from cryptography.hazmat.primitives.asymmetric.x25519 import (
    X25519PrivateKey,
    X25519PublicKey
)
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


# ==========================================
# CONFIGURATION
# ==========================================

ENCRYPTED_FILE = Path("output/sample.enc")
METADATA_FILE = Path("output/metadata.json")
PRIVATE_KEY_FILE = Path("output/private_keys.json")

DECRYPTED_FILE = Path("output/decrypted_sample.txt")


# ==========================================
# 1. LOAD METADATA
# ==========================================

metadata = json.loads(
    METADATA_FILE.read_text()
)

sender_x25519_public_bytes = base64.b64decode(
    metadata["x25519_sender_public_key"]
)

mlkem_ciphertext = base64.b64decode(
    metadata["mlkem_ciphertext"]
)

nonce = base64.b64decode(
    metadata["nonce"]
)

print("Public metadata loaded.")


# ==========================================
# 2. LOAD PRIVATE KEYS
# ==========================================

private_keys = json.loads(
    PRIVATE_KEY_FILE.read_text()
)

receiver_x25519_private_bytes = base64.b64decode(
    private_keys["x25519_receiver_private_key"]
)

receiver_mlkem_private = base64.b64decode(
    private_keys["mlkem_receiver_private_key"]
)

print("Private keys loaded.")


# ==========================================
# 3. RECONSTRUCT X25519 PRIVATE KEY
# ==========================================

receiver_x25519_private = (
    X25519PrivateKey.from_private_bytes(
        receiver_x25519_private_bytes
    )
)

sender_x25519_public = (
    X25519PublicKey.from_public_bytes(
        sender_x25519_public_bytes
    )
)


# ==========================================
# 4. X25519 SHARED SECRET
# ==========================================

x25519_secret = receiver_x25519_private.exchange(
    sender_x25519_public
)

print("X25519 shared secret reconstructed.")


# ==========================================
# 5. RECONSTRUCT ML-KEM SECRET
# ==========================================

kem = oqs.KeyEncapsulation(
    "ML-KEM-768",
    receiver_mlkem_private
)

mlkem_secret = kem.decap_secret(
    mlkem_ciphertext
)

print("ML-KEM-768 shared secret reconstructed.")


# ==========================================
# 6. COMBINE HYBRID SECRETS
# ==========================================

combined_secret = (
    x25519_secret +
    mlkem_secret
)


# ==========================================
# 7. HKDF → SAME AES-256 KEY
# ==========================================

hkdf = HKDF(
    algorithm=hashes.SHA256(),
    length=32,
    salt=None,
    info=b"HybridCrypto-AES-Key"
)

aes_key = hkdf.derive(
    combined_secret
)

print("Same hybrid AES-256 key reconstructed.")


# ==========================================
# 8. LOAD ENCRYPTED FILE
# ==========================================

encrypted_data = ENCRYPTED_FILE.read_bytes()

print(
    f"Encrypted file size: "
    f"{len(encrypted_data)} bytes"
)


# ==========================================
# 9. AES-256-GCM DECRYPTION
# ==========================================

aes = AESGCM(aes_key)

plaintext = aes.decrypt(
    nonce,
    encrypted_data,
    None
)


# ==========================================
# 10. SAVE DECRYPTED FILE
# ==========================================

DECRYPTED_FILE.write_bytes(
    plaintext
)

print(
    f"Decrypted file: "
    f"{DECRYPTED_FILE}"
)


# ==========================================
# 11. RESULT
# ==========================================

print(
    "SUCCESS: Hybrid decryption completed."
)