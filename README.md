# HexCrypt-Cli

A command-line tool for symmetric encryption and decryption of text and files using [Fernet](https://cryptography.io/en/latest/fernet/) (AES-128-CBC + HMAC-SHA256).

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```
python run.py COMMAND [options]
```

### Commands

| Command        | Description                          |
|----------------|--------------------------------------|
| `generate-key` | Generate a new encryption key        |
| `encrypt`      | Encrypt text or a file               |
| `decrypt`      | Decrypt a token or an encrypted file |

---

### generate-key

```bash
# Print the key to the terminal
python run.py generate-key

# Save the key to a file
python run.py generate-key -o my.key
```

---

### encrypt

```bash
# Encrypt text (key as string)
python run.py encrypt --key <KEY> -t "Hello, World!"

# Encrypt text (key from file)
python run.py encrypt --key-file my.key -t "Hello, World!"

# Encrypt a file (output defaults to <file>.enc)
python run.py encrypt --key-file my.key -f secret.txt

# Encrypt a file with a custom output path
python run.py encrypt --key-file my.key -f secret.txt -o secret.enc
```

---

### decrypt

```bash
# Decrypt a token
python run.py decrypt --key-file my.key -t "gAAAAAB..."

# Decrypt a file (output defaults to original name without .enc)
python run.py decrypt --key-file my.key -f secret.enc

# Decrypt a file with a custom output path
python run.py decrypt --key-file my.key -f secret.enc -o recovered.txt
```

---

## Quick Example

```bash
# 1. Generate and save a key
python run.py generate-key -o my.key

# 2. Encrypt some text
python run.py encrypt --key-file my.key -t "Top secret message"
# [✓] Encrypted token:
# gAAAAAB...

# 3. Decrypt it back
python run.py decrypt --key-file my.key -t "gAAAAAB..."
# [✓] Decrypted text:
# Top secret message
```

## Security Notes

- Keep your key file safe — anyone with the key can decrypt your data.
- Fernet guarantees confidentiality and integrity (authenticated encryption).
- Do not reuse keys across different sensitive contexts.
