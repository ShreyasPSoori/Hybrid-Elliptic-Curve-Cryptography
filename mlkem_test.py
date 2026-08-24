import oqs


# ==========================================
# ML-KEM-768
# ==========================================

kem = oqs.KeyEncapsulation("ML-KEM-768")


# ==========================================
# KEY GENERATION
# ==========================================

public_key = kem.generate_keypair()
private_key = kem.export_secret_key()

print("ML-KEM-768 key pair generated successfully.")


# ==========================================
# ENCAPSULATION
# ==========================================

ciphertext, sender_shared_secret = kem.encap_secret(public_key)

print("Encapsulation successful.")


# ==========================================
# DECAPSULATION
# ==========================================

receiver_shared_secret = kem.decap_secret(ciphertext)

print("Decapsulation successful.")


# ==========================================
# VERIFY
# ==========================================

if sender_shared_secret == receiver_shared_secret:
    print("SUCCESS: ML-KEM shared secrets match!")
else:
    print("ERROR: Shared secrets do not match.")