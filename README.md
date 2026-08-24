# Hybrid Elliptic Curve Cryptography for Cloud Data Security

## 1. Project Overview

This project proposes a hybrid cryptographic framework for secure encryption of data stored in cloud environments.

The system combines:

- AES-256-GCM for fast symmetric encryption of data
- X25519 for classical elliptic-curve key agreement
- ML-KEM-768 for post-quantum key encapsulation
- HKDF for deriving the final AES encryption key from hybrid secret material

The goal is to combine the performance of symmetric encryption with the security properties of classical and post-quantum public-key cryptography.

---

## 2. Current Implementation Status

| Component | Algorithm | Status |
|---|---|---|
| File Encryption | AES-256-GCM | ✅ Completed |
| Classical Key Agreement | X25519 | ✅ Completed |
| Post-Quantum Key Encapsulation | ML-KEM-768 | ✅ Completed |
| Hybrid Key Derivation | X25519 + ML-KEM + HKDF | 🔨 In Progress |
| Cloud Storage | TBD | ⏳ Planned |
| Key Management System (KMS) | TBD | ⏳ Planned |
| Data Integrity | SHA-256 | ⏳ Planned |
| Performance Evaluation | TBD | ⏳ Planned |


## 3. Project Structure
HybridCrypto/
│
├── .gitignore
├── README.md
├── aes_test.py
├── x25519_test.py
├── mlkem_test.py
│
├── input/
│   └── sample.txt
│
└── .venv/

## 4. Installation
Step 1: Clone the Repository
git clone https://github.com/ShreyasPSoori/Hybrid-Elliptic-Curve-Cryptography.git
cd Hybrid-Elliptic-Curve-Cryptography

Step 2: Create a Virtual Environment
python -m venv .venv

Step 3: Activate the Virtual Environment
Windows PowerShell
.venv\Scripts\Activate.ps1

If PowerShell blocks script execution:

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

Then activate again:

.venv\Scripts\Activate.ps1

Step 4: Install Python Packages
pip install cryptography
pip install liboqs-python

## 5. ML-KEM-768 Setup on Windows

liboqs-python requires the native liboqs library.

Required Tools

Install Visual Studio Build Tools with:

Desktop development with C++
MSVC C++ Build Tools
Windows SDK
CMake tools for Windows
Build liboqs

Clone the liboqs repository:

git clone https://github.com/open-quantum-safe/liboqs.git

Configure the build:

cmake -S C:\Users\<username>\liboqs -B C:\Users\<username>\liboqs\build -DBUILD_SHARED_LIBS=ON -DCMAKE_WINDOWS_EXPORT_ALL_SYMBOLS=TRUE

Build:

cmake --build C:\Users\<username>\liboqs\build --config Release --parallel

The resulting library should contain:

oqs.dll

The exact location may depend on the build configuration.

For the current Windows setup, the DLL is located under:

liboqs\build\bin\Release\oqs.dll

The directory containing oqs.dll must be available to Python through the system PATH.