# Project Template — HexCrypt-Cli

## Summary

`HexCrypt-Cli` is an open-source Python tool designed for symmetric encryption and decryption of text and files.  
It is built for developers, security engineers, and students who need a fast, reliable command-line interface for protecting sensitive data using industry-standard authenticated encryption.

---

# Purpose

This project exists to make strong encryption accessible directly from the terminal without writing any code.

This project helps developers and security practitioners to:

- Encrypt and decrypt sensitive text or files with a single command
- Safely manage and store encryption keys on disk
- Validate encryption workflows in scripts and automation pipelines
- Learn how Fernet symmetric encryption works in practice
- Integrate file-level encryption into DevSecOps or data handling workflows

---

# Technical Stack

| Component | Technology |
|---|---|
| Language | Python 3.10+ |
| Framework | Standard Library (`argparse`, `os`, `sys`) |
| Database | None |
| Networking | None (local operation only) |
| Concurrency | None |
| Logging | `sys.stderr` / stdout status messages |
| Configuration | CLI arguments |

---

# How It Works

1. The user generates a Fernet key using the `generate-key` subcommand — optionally saving it to a file
2. The key is passed to `encrypt` or `decrypt` via `--key` (inline) or `--key-file` (from disk)
3. For text mode, the plaintext is UTF-8 encoded, encrypted, and the resulting token is printed to stdout
4. For file mode, the source file is read as raw bytes, encrypted or decrypted, and written to the output path
5. On decryption, an `InvalidToken` error is caught and reported cleanly if the key is wrong or the token is corrupted

---

# Features

- Three subcommands: `generate-key`, `encrypt`, `decrypt`
- Encrypt and decrypt both plain text and arbitrary binary files
- Key management via inline string or key file (`--key` / `--key-file`)
- Sensible output path defaults (`.enc` suffix for encrypted files, stripped on decrypt)
- Clear, actionable error messages with no raw tracebacks
- Interactive fallback when no text or token argument is provided

---

# Configuration

All runtime behavior is controlled through CLI arguments — no config file or environment variables required.

| Argument | Description | Default |
|---|---|---|
| `--key` | Encryption/decryption key as a string | None |
| `--key-file` | Path to a file containing the key | None |
| `-t / --text` | Plain text to encrypt or token to decrypt | None (interactive prompt) |
| `-f / --file` | Source file to encrypt or decrypt | None |
| `-o / --output` | Output file path (file mode only) | `<input>.enc` or `<input>.dec` |

---

# Observable Signals / Telemetry

This tool operates entirely locally and produces no network traffic. Observable artifacts include:

- **Process execution** — Python interpreter launched with `run.py` and a subcommand as arguments
- **Filesystem activity** — Key files written to disk (`.key`), encrypted files with `.enc` extension
- **Stdout/stderr output** — Status messages prefixed with `[✓]` or `[✗]` for success and failure
- **Exit codes** — Non-zero exit on invalid key, missing file, or bad token
- **No network activity** — All operations are local; no data leaves the machine

---

# Detection Engineering Opportunities

Security teams can use this project to validate:

- File write monitoring rules (key file and `.enc` artifact creation)
- Process execution alerts for Python scripts handling cryptographic operations
- DLP policies around encrypted file creation and movement
- Insider threat scenarios involving local data encryption before exfiltration
- Alert triage for legitimate vs. malicious use of encryption utilities

---

# Project Structure

```text
HexCrypt-Cli/
├── run.py               # Main CLI entry point
├── requirements.txt     # Pinned dependencies
├── README.md            # Setup and usage guide
├── blog-post.md         # Technical deep dive (this file)
└── project-templates.md # Project documentation template
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

### Subcommands

```bash
python run.py generate-key                        # Print a new key
python run.py generate-key -o my.key             # Save key to file

python run.py encrypt --key-file my.key -t "Hello"          # Encrypt text
python run.py encrypt --key-file my.key -f report.pdf       # Encrypt file

python run.py decrypt --key-file my.key -t "gAAAAAB..."     # Decrypt token
python run.py decrypt --key-file my.key -f report.pdf.enc   # Decrypt file
```

Example output:

```text
[✓] Key saved to: my.key
[✓] Encrypted token:
gAAAAABmX3k2...
[✓] Decrypted text:
Hello
```

---

# Example Workflow

| Stage | Description |
|---|---|
| Key Generation | `generate-key` creates a 32-byte URL-safe base64 Fernet key |
| Encryption | Plaintext or file bytes are AES-128-CBC encrypted with HMAC-SHA256 |
| Token Output | Encrypted result is base64-encoded and printed or written to disk |
| Decryption | Token is verified (HMAC), decrypted, and returned as plaintext or file |
| Error Handling | Invalid key or corrupted token exits cleanly with a descriptive message |

---

# Intended Audience

- Developers needing quick file or text encryption in scripts
- Security engineers validating encryption in data pipelines
- Students learning applied cryptography
- DevSecOps engineers building secure automation workflows
- CTF participants and security researchers

---

# Security Considerations

Before using in any sensitive context:

- Store key files with restricted permissions (`chmod 600 my.key` on Unix)
- Do not pass keys as CLI arguments in shared or logged environments — use `--key-file` instead
- Fernet keys are symmetric — anyone with the key can decrypt your data
- This tool does not provide key exchange or asymmetric encryption
- Do not use the same key across unrelated sensitive datasets

---

# Ethical and Legal Notice

This project is provided for legitimate encryption, data protection, and educational purposes.

Use only on data you own or are explicitly authorized to handle. The authors assume no liability for misuse or data loss resulting from improper key management or deployment.

---

# Roadmap

- [ ] Add asymmetric encryption support (RSA / ECC)
- [ ] Add password-derived key generation (PBKDF2 / Argon2)
- [ ] Add directory encryption (recursive file mode)
- [ ] Add encrypted key storage (password-protected key files)
- [ ] Add Docker deployment
- [ ] Add `--verify` mode to check token integrity without decrypting

---

# Related Resources

- [Python cryptography library](https://cryptography.io/en/latest/)
- [Fernet specification](https://github.com/fernet/spec/blob/master/Spec.md)
- [OWASP Cryptographic Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)
- [NIST Guidelines on Cryptography](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines)

---

# License

This project is licensed under the [MIT License](LICENSE).

---

# Maintainer

**[Your Name / Alias]**  
[GitHub Profile]  
[Website or Portfolio]
