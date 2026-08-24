from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF


# ==========================================
# TEST SECRET MATERIAL
# ==========================================

x25519_secret = b"example-x25519-secret"

mlkem_secret = b"example-mlkem-secret"


# ==========================================
# COMBINE SECRET MATERIAL
# ==========================================

combined_secret = x25519_secret + mlkem_secret


# ==========================================
# HKDF
# ==========================================

hkdf = HKDF(
    algorithm=hashes.SHA256(),
    length=32,
    salt=None,
    info=b"HybridCrypto-AES-Key"
)


aes_key = hkdf.derive(combined_secret)


# ==========================================
# RESULT
# ==========================================

print("Hybrid key derivation successful.")
print("AES key length:", len(aes_key), "bytes")