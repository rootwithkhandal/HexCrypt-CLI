"""
Cryptography CLI Tool
Encrypt and decrypt text or files using Fernet symmetric encryption.
"""

import argparse
import sys
import os
from cryptography.fernet import Fernet, InvalidToken


# ── Key helpers ──────────────────────────────────────────────────────────────

def generate_key() -> bytes:
    """Generate a new Fernet key."""
    return Fernet.generate_key()


def save_key(key: bytes, path: str) -> None:
    """Write a key to a file."""
    with open(path, "wb") as f:
        f.write(key)
    print(f"[✓] Key saved to: {path}")


def load_key(path: str) -> bytes:
    """Read a key from a file."""
    if not os.path.exists(path):
        print(f"[✗] Key file not found: {path}", file=sys.stderr)
        sys.exit(1)
    with open(path, "rb") as f:
        return f.read().strip()


def resolve_key(key_arg: str | None, key_file_arg: str | None) -> bytes:
    """Return a key from either a raw string/bytes argument or a key file."""
    if key_file_arg:
        return load_key(key_file_arg)
    if key_arg:
        return key_arg.encode() if isinstance(key_arg, str) else key_arg
    print("[✗] Provide a key via --key or --key-file.", file=sys.stderr)
    sys.exit(1)


# ── Encrypt / Decrypt ────────────────────────────────────────────────────────

def encrypt_text(text: str, key: bytes) -> bytes:
    """Encrypt a UTF-8 string and return the token."""
    f = Fernet(key)
    return f.encrypt(text.encode())


def decrypt_text(token: bytes | str, key: bytes) -> str:
    """Decrypt a Fernet token and return the plaintext string."""
    if isinstance(token, str):
        token = token.encode()
    f = Fernet(key)
    return f.decrypt(token).decode()


def encrypt_file(src: str, dst: str, key: bytes) -> None:
    """Encrypt a file and write the result to dst."""
    if not os.path.exists(src):
        print(f"[✗] Source file not found: {src}", file=sys.stderr)
        sys.exit(1)
    f = Fernet(key)
    with open(src, "rb") as infile:
        data = infile.read()
    encrypted = f.encrypt(data)
    with open(dst, "wb") as outfile:
        outfile.write(encrypted)
    print(f"[✓] Encrypted file saved to: {dst}")


def decrypt_file(src: str, dst: str, key: bytes) -> None:
    """Decrypt a Fernet-encrypted file and write the result to dst."""
    if not os.path.exists(src):
        print(f"[✗] Source file not found: {src}", file=sys.stderr)
        sys.exit(1)
    f = Fernet(key)
    with open(src, "rb") as infile:
        data = infile.read()
    decrypted = f.decrypt(data)
    with open(dst, "wb") as outfile:
        outfile.write(decrypted)
    print(f"[✓] Decrypted file saved to: {dst}")


# ── CLI handlers ─────────────────────────────────────────────────────────────

def cmd_generate_key(args: argparse.Namespace) -> None:
    key = generate_key()
    if args.output:
        save_key(key, args.output)
    else:
        print(f"[✓] Generated key: {key.decode()}")
        print("    Save this key — you will need it to decrypt your data.")


def cmd_encrypt(args: argparse.Namespace) -> None:
    key = resolve_key(args.key, args.key_file)

    if args.file:
        out = args.output or args.file + ".enc"
        encrypt_file(args.file, out, key)
    elif args.text:
        token = encrypt_text(args.text, key)
        print(f"[✓] Encrypted token:\n{token.decode()}")
    else:
        # Interactive fallback
        text = input("Enter text to encrypt: ")
        token = encrypt_text(text, key)
        print(f"[✓] Encrypted token:\n{token.decode()}")


def cmd_decrypt(args: argparse.Namespace) -> None:
    key = resolve_key(args.key, args.key_file)

    try:
        if args.file:
            out = args.output or (
                args.file[:-4] if args.file.endswith(".enc") else args.file + ".dec"
            )
            decrypt_file(args.file, out, key)
        elif args.token:
            plaintext = decrypt_text(args.token, key)
            print(f"[✓] Decrypted text:\n{plaintext}")
        else:
            token = input("Enter encrypted token: ")
            plaintext = decrypt_text(token, key)
            print(f"[✓] Decrypted text:\n{plaintext}")
    except InvalidToken:
        print("[✗] Decryption failed — wrong key or corrupted token.", file=sys.stderr)
        sys.exit(1)


# ── Argument parser ───────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="hexcrypt-cli",
        description="Encrypt and decrypt text or files using Fernet symmetric encryption.",
    )
    subparsers = parser.add_subparsers(dest="command", metavar="COMMAND")
    subparsers.required = True

    # ── generate-key ──
    gk = subparsers.add_parser("generate-key", help="Generate a new encryption key.")
    gk.add_argument(
        "-o", "--output",
        metavar="FILE",
        help="Save the key to a file instead of printing it.",
    )
    gk.set_defaults(func=cmd_generate_key)

    # ── shared key options ──
    key_parent = argparse.ArgumentParser(add_help=False)
    key_group = key_parent.add_mutually_exclusive_group()
    key_group.add_argument("--key", metavar="KEY", help="Encryption key as a string.")
    key_group.add_argument(
        "--key-file", metavar="FILE", help="Path to a file containing the key."
    )

    # ── encrypt ──
    enc = subparsers.add_parser(
        "encrypt", parents=[key_parent], help="Encrypt text or a file."
    )
    enc_src = enc.add_mutually_exclusive_group()
    enc_src.add_argument("-t", "--text", metavar="TEXT", help="Plain text to encrypt.")
    enc_src.add_argument("-f", "--file", metavar="FILE", help="File to encrypt.")
    enc.add_argument(
        "-o", "--output", metavar="FILE", help="Output file path (file mode only)."
    )
    enc.set_defaults(func=cmd_encrypt)

    # ── decrypt ──
    dec = subparsers.add_parser(
        "decrypt", parents=[key_parent], help="Decrypt a token or a file."
    )
    dec_src = dec.add_mutually_exclusive_group()
    dec_src.add_argument(
        "-t", "--token", metavar="TOKEN", help="Encrypted token to decrypt."
    )
    dec_src.add_argument("-f", "--file", metavar="FILE", help="Encrypted file to decrypt.")
    dec.add_argument(
        "-o", "--output", metavar="FILE", help="Output file path (file mode only)."
    )
    dec.set_defaults(func=cmd_decrypt)

    return parser


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
