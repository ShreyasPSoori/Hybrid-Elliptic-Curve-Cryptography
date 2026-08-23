from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

# Generate a random 256-bit AES key
key = AESGCM.generate_key(bit_length=256)

print("AES-256 key generated successfully.")

# Create AES-GCM object
aes = AESGCM(key)

# Read the file
with open("input/sample.txt", "rb") as file:
    plaintext = file.read()

# AES-GCM requires a unique nonce
nonce = os.urandom(12)

# Encrypt
ciphertext = aes.encrypt(nonce, plaintext, None)

# Save nonce + ciphertext
with open("encrypted.bin", "wb") as file:
    file.write(nonce + ciphertext)

print("File encrypted successfully.")

# ---------------- DECRYPTION ----------------

# Read encrypted file
with open("encrypted.bin", "rb") as file:
    encrypted_data = file.read()

# Extract nonce
nonce = encrypted_data[:12]

# Extract ciphertext + authentication tag
ciphertext = encrypted_data[12:]

# Decrypt
decrypted = aes.decrypt(nonce, ciphertext, None)

# Save decrypted file
with open("decrypted.txt", "wb") as file:
    file.write(decrypted)

print("File decrypted successfully.")

# Verify
if plaintext == decrypted:
    print("SUCCESS: Original and decrypted files are identical.")
else:
    print("ERROR: Files are different.")