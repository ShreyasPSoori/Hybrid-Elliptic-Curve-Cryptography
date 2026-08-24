from cryptography.hazmat.primitives.asymmetric.x25519 import (
    X25519PrivateKey
)


# ==========================================
# ALICE
# ==========================================

alice_private_key = X25519PrivateKey.generate()
alice_public_key = alice_private_key.public_key()


# ==========================================
# BOB
# ==========================================

bob_private_key = X25519PrivateKey.generate()
bob_public_key = bob_private_key.public_key()


print("Alice key pair generated.")
print("Bob key pair generated.")


# ==========================================
# KEY EXCHANGE
# ==========================================

# Alice uses:
# Alice's private key + Bob's public key

alice_shared_secret = alice_private_key.exchange(
    bob_public_key
)


# Bob uses:
# Bob's private key + Alice's public key

bob_shared_secret = bob_private_key.exchange(
    alice_public_key
)


# ==========================================
# VERIFY
# ==========================================

print()
print("Alice shared secret:", alice_shared_secret.hex())
print("Bob shared secret:  ", bob_shared_secret.hex())

print()

if alice_shared_secret == bob_shared_secret:
    print("SUCCESS: Shared secrets match!")
else:
    print("ERROR: Shared secrets do not match!")