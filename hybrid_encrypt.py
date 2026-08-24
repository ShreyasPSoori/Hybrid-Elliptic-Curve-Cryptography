from pathlib import Path
import secrets

import oqs

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.x25519 import (
    X25519PrivateKey
)
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF


# ==========================================
# CONFIGURATION
# ==========================================

INPUT_FILE = Path("input/sample.txt")
ENCRYPTED_FILE = Path("output/sample.enc")

ENCRYPTED_FILE.parent.mkdir(exist_ok=True)


# ==========================================
# 1. X25519
# ==========================================

alice_private = X25519PrivateKey.generate()
alice_public = alice_private.public_key()

bob_private = X25519PrivateKey.generate()
bob_public = bob_private.public_key()

x25519_secret = alice_private.exchange(bob_public)

print("X25519 key agreement: SUCCESS")


# ==========================================
# 2. ML-KEM-768
# ==========================================

kem = oqs.KeyEncapsulation("ML-KEM-768")

mlkem_public_key = kem.generate_keypair()

ciphertext, mlkem_secret = kem.encap_secret(
    mlkem_public_key
)

# Verify ML-KEM decapsulation
mlkem_decapsulated_secret = kem.decap_secret(
    ciphertext
)

if mlkem_secret != mlkem_decapsulated_secret:
    raise RuntimeError(
        "ML-KEM shared secrets do not match!"
    )

print("ML-KEM-768 key encapsulation: SUCCESS")


# ==========================================
# 3. HYBRID KEY DERIVATION
# ==========================================

combined_secret = (
    x25519_secret +
    mlkem_secret
)

hkdf = HKDF(
    algorithm=hashes.SHA256(),
    length=32,
    salt=None,
    info=b"HybridCrypto-AES-Key"
)

aes_key = hkdf.derive(combined_secret)

print("Hybrid AES-256 key generated.")


# ==========================================
# 4. READ FILE
# ==========================================

plaintext = INPUT_FILE.read_bytes()

print(f"Input file size: {len(plaintext)} bytes")


# ==========================================
# 5. AES-256-GCM ENCRYPTION
# ==========================================

aes = AESGCM(aes_key)

# AES-GCM requires a unique nonce.
# 12 bytes is the standard size.

nonce = secrets.token_bytes(12)

ciphertext_file = aes.encrypt(
    nonce,
    plaintext,
    None
)


# Store nonce + encrypted data.
output_data = nonce + ciphertext_file

ENCRYPTED_FILE.write_bytes(output_data)

print("File encrypted successfully.")
print(f"Encrypted file: {ENCRYPTED_FILE}")


# ==========================================
# 6. DECRYPT THE FILE
# ==========================================

stored_data = ENCRYPTED_FILE.read_bytes()

stored_nonce = stored_data[:12]
stored_ciphertext = stored_data[12:]

decrypted_data = aes.decrypt(
    stored_nonce,
    stored_ciphertext,
    None
)


# ==========================================
# 7. VERIFY
# ==========================================

if decrypted_data == plaintext:
    print("SUCCESS: Decrypted data matches original file.")
else:
    print("ERROR: Decrypted data does not match!")