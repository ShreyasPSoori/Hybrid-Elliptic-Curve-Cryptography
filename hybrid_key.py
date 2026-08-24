from cryptography.hazmat.primitives.asymmetric.x25519 import (
    X25519PrivateKey
)
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
import oqs


# ==========================================
# 1. X25519 KEY AGREEMENT
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

# Verify decapsulation
mlkem_decapsulated_secret = kem.decap_secret(
    ciphertext
)

if mlkem_secret == mlkem_decapsulated_secret:
    print("ML-KEM-768 key encapsulation: SUCCESS")
else:
    raise RuntimeError("ML-KEM shared secrets do not match!")


# ==========================================
# 3. COMBINE THE TWO SECRETS
# ==========================================

combined_secret = (
    x25519_secret +
    mlkem_secret
)


# ==========================================
# 4. HKDF → AES-256 KEY
# ==========================================

hkdf = HKDF(
    algorithm=hashes.SHA256(),
    length=32,
    salt=None,
    info=b"HybridCrypto-AES-Key"
)

aes_key = hkdf.derive(combined_secret)


# ==========================================
# 5. RESULT
# ==========================================

print("Hybrid key derivation: SUCCESS")
print("AES-256 key generated.")
print("AES key length:", len(aes_key), "bytes")