# Hybrid Elliptic Curve Cryptography for Cloud Data Security

## 1. Project Overview

This project proposes a hybrid cryptographic framework for securing data stored in cloud environments.

The project combines classical cryptography, post-quantum cryptography, and symmetric encryption to provide both strong security and efficient encryption of large data files.

The main cryptographic components are:

- **AES-256-GCM** – used for fast encryption of the actual data.
- **X25519** – used for classical elliptic-curve key agreement.
- **ML-KEM-768** – used for post-quantum key encapsulation.
- **HKDF** – planned for deriving the final AES encryption key from the hybrid secret material.

### Main Idea

Symmetric encryption such as AES is very fast and is suitable for encrypting large files.

Public-key cryptography is useful for securely establishing or protecting encryption keys, but it is generally slower for large amounts of data.

Therefore, the proposed system uses:

```text
Large File
    |
    v
AES-256-GCM
    |
    v
Encrypted File
```

The AES key will be derived using hybrid key material obtained from:

```text
X25519
   +
ML-KEM-768
   |
   v
  HKDF
   |
   v
AES-256 Key
```

The final system is intended to provide protection against current classical attacks while also incorporating post-quantum cryptography.

---

# 2. Objectives

The main objectives of the project are:

1. Securely encrypt data before storing it in the cloud.
2. Use AES-256-GCM for efficient encryption of large files.
3. Use X25519 for classical elliptic-curve key agreement.
4. Use ML-KEM-768 as a post-quantum key encapsulation mechanism.
5. Combine classical and post-quantum secret material using HKDF.
6. Implement secure key management for the cloud environment.
7. Verify data integrity using hashing.
8. Evaluate encryption and decryption performance.
9. Compare the performance of classical, post-quantum, and hybrid approaches.

---

# 3. Current Implementation Status

| Component | Algorithm / Technology | Status |
|---|---|---|
| File Encryption | AES-256-GCM | ✅ Completed |
| Classical Key Agreement | X25519 | ✅ Completed |
| Post-Quantum Key Encapsulation | ML-KEM-768 | ✅ Completed |
| Hybrid Key Derivation | X25519 + ML-KEM-768 + HKDF | 🔨 In Progress |
| Complete Hybrid Encryption | X25519 + ML-KEM + HKDF + AES | ⏳ Planned |
| Data Integrity | SHA-256 | ⏳ Planned |
| Cloud Storage | TBD | ⏳ Planned |
| Key Management System (KMS) | TBD | ⏳ Planned |
| Performance Evaluation | TBD | ⏳ Planned |

> **Important:** The current repository contains independently tested cryptographic components. The complete hybrid encryption workflow is still under development.

---

# 4. Cryptographic Algorithms

## 4.1 AES-256-GCM

AES is a symmetric encryption algorithm.

It uses the same secret key for encryption and decryption.

AES-256-GCM is used to encrypt the actual file because symmetric encryption is fast and suitable for large amounts of data.

```text
                AES-256-GCM

Input File
    |
    | AES Key
    v
Encryption
    |
    v
Encrypted File
    |
    | AES Key
    v
Decryption
    |
    v
Original File
```

The current implementation generates an AES-256 key and uses AES-GCM to encrypt and decrypt a test file.

---

## 4.2 X25519

X25519 is an elliptic-curve Diffie-Hellman key agreement mechanism.

It allows two parties to establish a shared secret without directly transmitting the secret.

Each party has:

```text
Private Key
Public Key
```

Example:

```text
Alice                              Bob

Private Key A                  Private Key B
Public Key A                   Public Key B
     |                              |
     |------ Public Key A --------> |
     | <------- Public Key B ------|
     |                              |
     v                              v

Private A + Public B          Private B + Public A
          |                            |
          v                            v
      Shared Secret A             Shared Secret B

              Shared Secret A
                     ==
              Shared Secret B
```

The current implementation verifies that both parties generate the same shared secret.

---

## 4.3 ML-KEM-768

ML-KEM-768 is a post-quantum Key Encapsulation Mechanism (KEM).

It is designed to provide key establishment that is resistant to attacks from future quantum computers.

The basic process is:

```text
Receiver
    |
    | Generate Key Pair
    |
    +---- Public Key
    |
    +---- Private Key


Sender
    |
    | Receiver's Public Key
    v
Encapsulation
    |
    +---- Ciphertext
    |
    +---- Shared Secret


Receiver
    |
    | Private Key + Ciphertext
    v
Decapsulation
    |
    v
Same Shared Secret
```

The current implementation uses ML-KEM-768 and verifies that the shared secret generated during encapsulation matches the secret recovered during decapsulation.

---

# 5. Hybrid Cryptographic Architecture

The final system will combine X25519 and ML-KEM-768.

```text
                    Input File
                        |
                        v
                 AES-256-GCM
                        |
                        v
                 Encrypted File
                        |
                     AES Key
                        |
                        v
                      HKDF
                        ^
                        |
             +----------+----------+
             |                     |
             |                     |
          X25519                ML-KEM-768
             |                     |
             v                     v
        Shared Secret 1       Shared Secret 2
             |                     |
             +----------+----------+
                        |
                        v
                       HKDF
                        |
                        v
                 AES-256 Key
```

### Planned Key Flow

```text
X25519
   |
   v
Classical Shared Secret
   |
   |
ML-KEM-768
   |
   v
Post-Quantum Shared Secret
   |
   +------------------+
                      |
                      v
                    HKDF
                      |
                      v
               AES-256 Key
                      |
                      v
                 AES-GCM
                      |
                      v
                Encrypted File
```

The purpose of this hybrid design is to combine:

- Classical elliptic-curve security
- Post-quantum security
- High-performance symmetric encryption

---

# 6. Why Use a Hybrid Approach?

Using only AES is efficient for file encryption, but AES itself does not solve the problem of securely establishing or protecting the encryption key between parties.

Using only public-key cryptography for large files would be inefficient.

Therefore:

```text
Public-Key / KEM Algorithms
        |
        | Secure key establishment
        v
    AES-256-GCM
        |
        | Fast data encryption
        v
    Large File
```

The proposed hybrid approach uses:

### X25519

Provides classical elliptic-curve key agreement.

### ML-KEM-768

Provides post-quantum key encapsulation.

### HKDF

Derives key material from the shared secrets.

### AES-256-GCM

Encrypts the actual data efficiently.

---

# 7. Project Structure

The current project structure is:

```text
HybridCrypto/
│
├── .gitignore
├── README.md
├── requirements.txt
│
├── aes_test.py
├── x25519_test.py
├── mlkem_test.py
│
└── input/
    └── sample.txt
```

### Important

The following are intentionally **not stored in GitHub**:

```text
.venv/
liboqs/
private keys
.env files
generated encrypted files
```

These files are ignored using `.gitignore` or are generated locally.

---

# 8. Technologies Used

## Programming Language

- Python 3

## Cryptographic Libraries

- `cryptography`
- `liboqs-python`
- Open Quantum Safe `liboqs`

## Development Tools

- Visual Studio Code
- Git
- GitHub
- CMake
- Microsoft Visual C++ Build Tools

---

# 9. Installation

## Step 1: Install Python

Install Python 3 from:

https://www.python.org/

Verify:

```powershell
python --version
```

---

## Step 2: Install Git

Install Git from:

https://git-scm.com/

Verify:

```powershell
git --version
```

---

## Step 3: Clone the Repository

```powershell
git clone https://github.com/ShreyasPSoori/Hybrid-Elliptic-Curve-Cryptography.git
```

Enter the project directory:

```powershell
cd Hybrid-Elliptic-Curve-Cryptography
```

---

# 10. Create the Python Virtual Environment

Create the virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

You should see:

```text
(.venv) PS E:\HybridCrypto>
```

---

## PowerShell Execution Policy Error

If you get an error saying that script execution is disabled, run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate again:

```powershell
.venv\Scripts\Activate.ps1
```

---

# 11. Install Python Dependencies

The required Python packages are listed in `requirements.txt`.

Install them using:

```powershell
pip install -r requirements.txt
```

The current requirements are:

```text
cryptography==50.0.0
liboqs-python==0.16.0
```

---

# 12. ML-KEM-768 Setup on Windows

`liboqs-python` provides Python bindings for the native `liboqs` library.

On Windows, the native library needs to be built using CMake and a C/C++ compiler.

## Required Tools

Install:

- Visual Studio Build Tools
- Desktop development with C++
- MSVC C++ Build Tools
- Windows SDK
- CMake tools for Windows

The official `liboqs-python` documentation also recommends using a Visual Studio Developer Command Prompt on Windows when building `liboqs`.

---

# 13. Clone liboqs

Do **not** clone `liboqs` inside the project repository.

For example:

```text
C:\Users\<username>\liboqs
```

Clone it using:

```cmd
cd /d C:\Users\<username>
git clone https://github.com/open-quantum-safe/liboqs.git
```

---

# 14. Configure liboqs

Open a **Developer Command Prompt for Visual Studio**.

Verify that CMake is available:

```cmd
cmake --version
```

Verify that the MSVC compiler is available:

```cmd
cl
```

Configure the build:

```cmd
cmake -S C:\Users\<username>\liboqs -B C:\Users\<username>\liboqs\build -DBUILD_SHARED_LIBS=ON -DCMAKE_WINDOWS_EXPORT_ALL_SYMBOLS=TRUE
```

The important option for Windows is:

```text
-DCMAKE_WINDOWS_EXPORT_ALL_SYMBOLS=TRUE
```

---

# 15. Build liboqs

Run:

```cmd
cmake --build C:\Users\<username>\liboqs\build --config Release --parallel
```

After a successful build, the shared library should be available under a path similar to:

```text
C:\Users\<username>\liboqs\build\bin\Release\oqs.dll
```

The exact location can depend on the build configuration.

---

# 16. Make oqs.dll Available to Python

In the VS Code PowerShell terminal where the project is being tested, temporarily add the directory containing `oqs.dll` to `PATH`.

Example:

```powershell
$env:PATH = "C:\Users\<username>\liboqs\build\bin\Release;$env:PATH"
```

Verify the DLL:

```powershell
where.exe oqs.dll
```

It should show something similar to:

```text
C:\Users\<username>\liboqs\build\bin\Release\oqs.dll
```

---

# 17. Verify ML-KEM-768

Run:

```powershell
python -c "import oqs; print(oqs.get_enabled_kem_mechanisms())"
```

The output should contain:

```text
ML-KEM-768
```

If `ML-KEM-768` appears, the post-quantum environment is ready.

---

# 18. Testing the Current Implementation

The project currently contains three independent tests.

---

## 18.1 AES-256-GCM Test

Run:

```powershell
python aes_test.py
```

Expected output:

```text
AES-256 key generated successfully.
File encrypted successfully.
File decrypted successfully.
SUCCESS: Original and decrypted files are identical.
```

This verifies that:

1. An AES-256 key is generated.
2. The file is encrypted.
3. The encrypted file is decrypted.
4. The decrypted file matches the original file.

---

## 18.2 X25519 Test

Run:

```powershell
python x25519_test.py
```

Expected output:

```text
Alice key pair generated.
Bob key pair generated.

SUCCESS: Shared secrets match!
```

This verifies that both parties independently derive the same X25519 shared secret.

---

## 18.3 ML-KEM-768 Test

Run:

```powershell
python mlkem_test.py
```

Expected output:

```text
ML-KEM-768 key pair generated successfully.
Encapsulation successful.
Decapsulation successful.
SUCCESS: ML-KEM shared secrets match!
```

This verifies that the secret obtained during encapsulation matches the secret obtained during decapsulation.

---

# 19. Current Development Workflow

The project uses Git and GitHub for collaborative development.

Before starting work:

```powershell
git pull
```

Check the repository:

```powershell
git status
```

Create a feature branch:

```powershell
git checkout -b feature/<feature-name>
```

Example:

```powershell
git checkout -b feature/hybrid-kdf
```

After making changes:

```powershell
git status
git add .
git commit -m "Implement hybrid key derivation"
git push -u origin feature/hybrid-kdf
```

Then create a Pull Request on GitHub.

---

# 20. Security Rules

Never commit sensitive information to GitHub.

Do not upload:

```text
Private keys
AES keys
Shared secrets
Cloud credentials
API keys
.env files
Passwords
Certificates containing private keys
```

The `.gitignore` file helps prevent accidental commits of sensitive or generated files.

### Never print secret material in the final implementation.

The current cryptographic test programs only verify whether secrets match. Actual secret values should not be printed or exposed in production code.

---

# 21. Planned Complete System

The final project will extend the current implementation into a complete cloud security workflow.

The planned process is:

```text
                         User
                           |
                           | Upload File
                           v
                    Data Preprocessing
                           |
                           v
                     File / Data
                           |
                           v
                     AES-256-GCM
                           |
                           v
                  Encrypted File
                           |
                           v
                    Cloud Storage
```

The AES encryption key will be derived using hybrid cryptographic key material:

```text
                 X25519
                    |
                    v
           Classical Secret
                    |
                    |
                 ML-KEM-768
                    |
                    v
          Post-Quantum Secret
                    |
                    v
                   HKDF
                    |
                    v
              AES-256 Key
```

Future components will include:

```text
                    Cloud System
                         |
          +--------------+--------------+
          |                             |
          v                             v
   Encrypted Data                  Key Management
   / File Storage                      System
          |                             |
          |                             |
          +-------------+---------------+
                        |
                        v
                 Secure Retrieval
                        |
                        v
                  Decryption
                        |
                        v
                 Original File
```

---

# 22. Planned Key Management System

A Key Management System (KMS) will be incorporated in the later implementation.

The KMS will be responsible for tasks such as:

- Secure key storage
- Key generation
- Key retrieval
- Key rotation
- Access control
- Separation of encryption keys from encrypted data

The exact cloud platform and KMS implementation will be finalized during the cloud integration phase.

---

# 23. Planned Data Integrity

SHA-256 hashing will be added to verify data integrity.

The planned process is:

```text
Original File
     |
     v
SHA-256
     |
     v
Original Hash
```

After retrieving and decrypting the file:

```text
Decrypted File
      |
      v
   SHA-256
      |
      v
Decrypted Hash
```

Then:

```text
Original Hash == Decrypted Hash
             |
       +-----+-----+
       |           |
      Yes          No
       |           |
    Integrity     Data
    Verified      Changed
```

---

# 24. Planned Performance Evaluation

The final system will be evaluated using different file sizes and file types.

Possible test files include:

- Text files
- PDF documents
- Images
- Videos
- Large datasets

Performance measurements may include:

- Key generation time
- Key encapsulation time
- Key decapsulation time
- Encryption time
- Decryption time
- Total processing time
- Throughput
- Memory usage

The hybrid approach will be compared with relevant classical and post-quantum approaches.

---

# 25. Future Work

The following features are planned:

1. Combine X25519 and ML-KEM-768 using HKDF.
2. Derive the final AES-256 encryption key.
3. Integrate hybrid key derivation with AES-256-GCM.
4. Implement complete file encryption and decryption.
5. Add SHA-256 integrity verification.
6. Add cloud storage.
7. Implement a Key Management System.
8. Add access control.
9. Implement secure key retrieval.
10. Evaluate different file sizes and file types.
11. Measure encryption and decryption performance.
12. Compare classical, post-quantum, and hybrid approaches.
13. Optimize the system for large cloud data.

---

# 26. Current Project Milestone

At the current stage, the following components have been successfully implemented and tested:

```text
AES-256-GCM
      |
      +---- File encryption/decryption       ✅


X25519
      |
      +---- Shared secret generation         ✅


ML-KEM-768
      |
      +---- Encapsulation/decapsulation      ✅
```

The next major milestone is:

```text
X25519 Shared Secret
          +
ML-KEM-768 Shared Secret
          |
          v
         HKDF
          |
          v
    AES-256 Encryption Key
          |
          v
     AES-256-GCM
          |
          v
      File Encryption
```

---

# 27. References

### Open Quantum Safe – liboqs

https://github.com/open-quantum-safe/liboqs

### Open Quantum Safe – liboqs-python

https://github.com/open-quantum-safe/liboqs-python

### Project Repository

https://github.com/ShreyasPSoori/Hybrid-Elliptic-Curve-Cryptography