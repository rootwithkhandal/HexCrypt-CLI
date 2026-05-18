# Project Template — HexCrypt-Cli

## Summary

`HexCrypt-Cli` is an open-source Python tool designed for symmetric encryption and decryption of text and files from the command line.  
It is built for developers, security engineers, and students working in local or automated environments and focuses on providing fast, authenticated encryption using the Fernet standard with a clean, scriptable interface.

---

# Purpose

This project exists to remove the friction of applying strong encryption without writing boilerplate code.

This project helps developers and security practitioners to:

- Encrypt sensitive text or files with a single terminal command
- Safely generate, store, and reuse encryption keys on disk
- Integrate file-level encryption into scripts and automation pipelines
- Understand and apply Fernet symmetric encryption in real workflows
- Protect data at rest without depending on external services or GUIs

---

# Technical Stack

| Component | Technology |
|---|---|
| Language | Python 3.10+ |
| Framework | Standard Library (`argparse`, `os`, `sys`) |
| Database | None |
| Networking | None (fully local) |
| Concurrency | None |
| Logging | stdout / stderr status messages |
| Configuration | CLI arguments (`--key`, `--key-file`, `--output`) |

---

# How It Works

1. The user runs `generate-key` to produce a new Fernet key, optionally saving it to a file with `-o`
2. The key is supplied to `encrypt` or `decrypt` via `--key` (inline string) or `--key-file` (path to key file)
3. In text mode, the input string is UTF-8 encoded, encrypted, and the base64 token is printed to stdout
4. In file mode, the source file is read as raw bytes, encrypted or decrypted, and written to the output path
5. On decryption failure, an `InvalidToken` exception is caught and reported with a clear error message — no raw traceback

---

# Features

- Three focused subcommands: `generate-key`, `encrypt`, `decrypt`
- Text and binary file encryption/decryption support
- Flexible key input: inline string (`--key`) or key file (`--key-file`)
- Smart output path defaults — `.enc` appended on encrypt, stripped on decrypt
- Interactive prompt fallback when no text or token argument is provided
- Clean `[✓]` / `[✗]` status output and non-zero exit codes on failure

---

# Configuration

All behavior is controlled through CLI arguments. No config file or environment variables are required.

| Argument | Description | Default |
|---|---|---|
| `--key` | Encryption/decryption key as an inline string | None |
| `--key-file` | Path to a file containing the key | None |
| `-t / --text` | Plain text to encrypt, or token to decrypt | None (interactive prompt) |
| `-f / --file` | Source file path to encrypt or decrypt | None |
| `-o / --output` | Destination file path (file mode only) | `<input>.enc` or `<input>.dec` |

---

# Observable Signals / Telemetry

This tool is fully local and produces no network traffic. Observable artifacts include:

- **Process execution** — Python interpreter launched with `run.py` and a subcommand as arguments
- **Filesystem activity** — Key files (`.key`), encrypted output files (`.enc`), decrypted output files
- **Stdout/stderr output** — Prefixed status lines (`[✓]` success, `[✗]` failure)
- **Exit codes** — Non-zero on invalid key, missing file, or corrupted token
- **No network activity** — All operations are local; nothing leaves the machine

---

# Detection Engineering Opportunities

Security teams can use this project to validate:

- File write monitoring for `.key` and `.enc` artifact creation
- Process execution alerts for Python scripts performing cryptographic operations
- DLP policies around encrypted file creation and movement
- Insider threat scenarios involving local data encryption prior to exfiltration
- Distinguishing legitimate encryption tooling from malicious ransomware-like behavior

---

# Project Structure

```text
HexCrypt-Cli/
├── run.py                   # Main CLI entry point
├── requirements.txt         # Pinned dependencies
├── README.md                # Setup and usage guide
├── blog-post.md             # Technical deep dive
├── project-description.md   # Project overview (this file)
└── project-templates.md     # Documentation template
```

---

# Installation

## Clone the repository

```bash
git clone https://github.com/[username]/HexCrypt-Cli.git
cd HexCrypt-Cli
```

## Install dependencies

```bash
pip install -r requirements.txt
```

---

# Usage

```bash
python run.py COMMAND [options]
```

Example output:

```text
[✓] Key saved to: my.key
[✓] Encrypted token:
gAAAAABmX3k2...
[✓] Decrypted text:
Hello, World!
```

---

# Example Workflow

| Stage | Description |
|---|---|
| Key Generation | `generate-key` produces a 32-byte URL-safe base64 Fernet key |
| Encryption | Input is AES-128-CBC encrypted with an HMAC-SHA256 integrity tag |
| Token Output | Result is base64-encoded and printed to stdout or written to a file |
| Decryption | Token HMAC is verified, then decrypted and returned as plaintext or file |
| Error Handling | Wrong key or corrupted token exits with `[✗]` message and code 1 |

---

# Intended Audience

- Developers needing quick text or file encryption in scripts
- Security engineers validating encryption in data handling pipelines
- Students learning applied cryptography and CLI tool design
- DevSecOps engineers building secure automation workflows
- CTF participants and security researchers

---

# Security Considerations

Before using in any sensitive context:

- Store key files with restricted permissions (`chmod 600 my.key` on Unix)
- Prefer `--key-file` over `--key` to avoid keys appearing in shell history or process lists
- Fernet is symmetric — anyone with the key can decrypt your data; protect it accordingly
- This tool does not provide key exchange, asymmetric encryption, or key rotation
- Do not reuse the same key across unrelated sensitive datasets

---

# Ethical and Legal Notice

This project is provided for legitimate encryption, data protection, and educational purposes.

Use only on data you own or are explicitly authorized to handle. The authors assume no liability for misuse, data loss, or damages resulting from improper key management or deployment.

---

# Roadmap

- [ ] Add asymmetric encryption support (RSA / ECC)
- [ ] Add password-derived key generation (PBKDF2 / Argon2)
- [ ] Add recursive directory encryption
- [ ] Add password-protected key file storage
- [ ] Add `--verify` mode to check token integrity without decrypting
- [ ] Add Docker deployment support

---

# Related Resources

- [Python cryptography library](https://cryptography.io/en/latest/)
- [Fernet specification](https://github.com/fernet/spec/blob/master/Spec.md)
- [OWASP Cryptographic Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)
- [NIST Cryptographic Standards and Guidelines](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines)

---

# License

This project is licensed under the [MIT License](LICENSE).

---

# Maintainer

**[Your Name / Alias]**  
[GitHub Profile]  
[Website or Portfolio]
