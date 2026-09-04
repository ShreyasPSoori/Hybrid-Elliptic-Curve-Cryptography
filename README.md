# Hybrid Elliptic-Curve Cryptography for Secure File Exchange

An educational prototype that demonstrates secure file exchange between two users by combining classical, post-quantum, and symmetric cryptography.

## Overview

The system models a secure file exchange between two users:

- **Alice (sender)** selects a file and encrypts it before transmission.
- **Bob (receiver)** receives the encrypted file and public metadata, then decrypts it using his private key material.

| Purpose | Technology |
| --- | --- |
| Fast file encryption | AES-256-GCM |
| Classical key agreement | X25519 |
| Post-quantum key encapsulation | ML-KEM-768 |
| Key derivation | HKDF-SHA256 |

AES-GCM protects the file contents. X25519 and ML-KEM-768 establish two independent shared secrets. HKDF combines those secrets into the final 256-bit AES key.

## Two-User Exchange

```text
                         ALICE / SENDER
                              |
                    Generate ephemeral X25519 keys
                              |
              Encapsulate ML-KEM using Bob's public key
                              |
                 X25519 secret + ML-KEM secret
                              |
                         HKDF-SHA256
                              |
                         AES-256 key
                              |
                   Encrypt file with AES-GCM
                              |
             Encrypted file + public metadata are sent
                              |
                              v
                         BOB / RECEIVER
                              |
                Bob's private X25519 and ML-KEM keys
                              |
              Reconstruct the same two shared secrets
                              |
                         HKDF-SHA256
                              |
                  Reconstruct the same AES key
                              |
                   Decrypt and verify the file
```

### What Alice Sends

Alice does **not** send the plaintext file or her private keys. The transferable package contains:

1. The encrypted file (`.enc`)
2. Public metadata containing the algorithm, nonce, and ML-KEM ciphertext
3. Alice's ephemeral X25519 public key

### What Bob Keeps Private

Bob keeps his X25519 private key and ML-KEM private key locally. Bob uses those keys with Alice's public key and the ML-KEM ciphertext to reconstruct the same hybrid secret material.

## Cryptographic Flow

### 1. Alice encrypts the file

Alice reads the input file as bytes. AES-256-GCM encrypts those bytes using a key derived from the hybrid secrets. Processing raw bytes supports text files, PDFs, DOCX files, images, videos, and other binary formats.

### 2. X25519 creates the classical shared secret

Alice generates an ephemeral X25519 key pair and uses Bob's X25519 public key. Bob later uses his private key with Alice's public key. Both sides calculate the same shared secret without transmitting that secret.

### 3. ML-KEM-768 creates the post-quantum shared secret

Bob's ML-KEM public key is used for encapsulation. Alice obtains an ML-KEM shared secret and sends the resulting KEM ciphertext. Bob uses his ML-KEM private key to decapsulate the ciphertext and recover the same shared secret.

### 4. HKDF derives the AES key

The X25519 and ML-KEM shared secrets are combined and passed to HKDF-SHA256. HKDF derives the 32-byte AES-256 key used for file encryption and decryption.

```text
X25519 shared secret
          +
ML-KEM-768 shared secret
          |
          v
      HKDF-SHA256
          |
          v
       AES-256 key
          |
          v
      AES-256-GCM
          |
          v
     Encrypted file
```

## Repository Structure

```text
Hybrid-Elliptic-Curve-Cryptography/
|
|-- hybrid_encrypt_v2.py       # Sender-side hybrid encryption prototype
|-- hybrid_decrypt_v2.py       # Receiver-side hybrid decryption prototype
|-- hybrid_key.py              # Hybrid key experiments
|-- aes_test.py                # AES-GCM test
|-- x25519_test.py             # X25519 shared-secret test
|-- mlkem_test.py              # ML-KEM encapsulation test
|-- hybrid_kdf_test.py         # Hybrid KDF test
|-- requirements.txt           # Python dependencies
|-- input/
|   `-- sample.txt
`-- frontend/
    |-- index.html              # Sender/Receiver role selector
    |-- sender.html             # Alice's file encryption page
    |-- receiver.html           # Bob's file decryption page
    |-- app.js                  # Frontend file and package logic
    `-- styles.css              # Shared frontend styling
```

## Current Implementation Status

| Component | Status | Notes |
| --- | --- | --- |
| AES-256-GCM file encryption/decryption | Complete | Tested with file bytes |
| X25519 key agreement | Complete | Shared secrets are compared |
| ML-KEM-768 encapsulation/decapsulation | Complete | Shared secrets are compared |
| X25519 + ML-KEM + HKDF integration | Prototype | Implemented in the v2 scripts |
| Two-user demonstration frontend | Complete | Sender and Receiver pages are available |
| SHA-256 file hashing | Planned | Additional integrity reporting |
| Cloud storage | Planned | Encrypted files only should be stored |
| Key Management System | Planned | Private-key protection and rotation |

> The Python scripts are the cryptographic prototype. The browser frontend is a demonstration interface and currently uses Web Crypto AES-GCM for its local file-byte demonstration. It does not replace the Python ML-KEM implementation.

## Frontend Demonstration

The frontend shows the two-user workflow without requiring a server.

### Alice: Sender Page

Open [`frontend/sender.html`](frontend/sender.html). Alice can:

1. Select any file up to 5 MB.
2. Encrypt the file in the browser demonstration.
3. Download the encrypted `.enc` file.
4. Download `metadata.json`.
5. Download `public-key.txt`.

Alice sends those three artifacts to Bob. The original file is never included as a plaintext download.

### Bob: Receiver Page

Open [`frontend/receiver.html`](frontend/receiver.html). Bob has separate spaces for:

1. The encrypted file
2. Metadata
3. Public key

The page checks that the package identifiers match. After verification, Bob can download the recovered file with its original filename and file type.

To open the role selector:

```powershell
start .\frontend\index.html
```

## Installation

### Python

Create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
pip install -r requirements.txt
```

```text
cryptography==50.0.0
liboqs-python==0.16.0
```

### Windows ML-KEM Setup

`liboqs-python` requires the native `liboqs` library. On Windows, install Visual Studio Build Tools with Desktop development with C++, the Windows SDK, and CMake.

Clone and build `liboqs` outside this repository:

```cmd
cd /d C:\Users\<username>
git clone https://github.com/open-quantum-safe/liboqs.git
cmake -S C:\Users\<username>\liboqs -B C:\Users\<username>\liboqs\build -DBUILD_SHARED_LIBS=ON -DCMAKE_WINDOWS_EXPORT_ALL_SYMBOLS=TRUE
cmake --build C:\Users\<username>\liboqs\build --config Release --parallel
```

Make the directory containing `oqs.dll` available to the current PowerShell session:

```powershell
$env:PATH = "C:\Users\<username>\liboqs\build\bin\Release;$env:PATH"
```

Verify that ML-KEM-768 is available:

```powershell
python -c "import oqs; print('ML-KEM-768' in oqs.get_enabled_kem_mechanisms())"
```

## Running the Python Prototype

Run the sender-side encryption prototype:

```powershell
python hybrid_encrypt_v2.py
```

This creates the prototype output package under `output/`, including the encrypted file, public metadata, and local receiver key material.

Run the receiver-side decryption prototype:

```powershell
python hybrid_decrypt_v2.py
```

The receiver reconstructs the X25519 and ML-KEM secrets, derives the AES key with HKDF, and decrypts the file.

## Component Tests

```powershell
python aes_test.py
python x25519_test.py
python mlkem_test.py
python hybrid_kdf_test.py
```

These tests verify AES encryption/decryption, matching X25519 shared secrets, matching ML-KEM shared secrets, and hybrid key derivation behavior.

## Security Notes

- Never commit private keys, AES keys, shared secrets, credentials, or generated output files.
- Never upload Bob's private keys with the encrypted file.
- Use a KMS or equivalent protected key store for a production deployment.
- Use authenticated encryption and handle decryption failures without exposing partial output.
- The current browser page is a demonstration. Production cryptography should use the reviewed Python backend or another reviewed cryptographic service.

## Planned Extensions

1. Connect the Sender and Receiver frontend to the Python hybrid encryption service.
2. Add SHA-256 file hashing and visible integrity comparison.
3. Add protected key storage and key rotation through a KMS.
4. Add authenticated users and access control.
5. Add cloud storage for encrypted files only.
6. Measure encryption and decryption performance across file sizes and formats.

## References

- [Open Quantum Safe liboqs](https://github.com/open-quantum-safe/liboqs)
- [Open Quantum Safe liboqs-python](https://github.com/open-quantum-safe/liboqs-python)
- [Project repository](https://github.com/ShreyasPSoori/Hybrid-Elliptic-Curve-Cryptography)
