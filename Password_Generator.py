#!/usr/bin/env python3
"""
password_generator.py
Simple secure password generator (CLI + function).
"""

import argparse
import secrets
import string
import sys

# Optional clipboard support (only used if user requests it)
try:
    import pyperclip
    PYPERCLIP_AVAILABLE = True
except Exception:
    PYPERCLIP_AVAILABLE = False

AMBIGUOUS = {'l', 'I', '1', '0', 'O', 'o'}

def build_charset(use_lower=True, use_upper=True, use_digits=True, use_symbols=True, avoid_ambiguous=False):
    charset = ''
    if use_lower:
        charset += string.ascii_lowercase
    if use_upper:
        charset += string.ascii_uppercase
    if use_digits:
        charset += string.digits
    if use_symbols:
        # A reasonable set of symbols. You can change or expand this.
        charset += "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
    if avoid_ambiguous:
        charset = ''.join(ch for ch in charset if ch not in AMBIGUOUS)
    if not charset:
        raise ValueError("Character set is empty. Enable at least one of lower/upper/digits/symbols.")
    return charset

def generate_password(length=16, charset=None):
    if charset is None:
        charset = build_charset()
    # Use secrets.choice for cryptographically secure randomness
    return ''.join(secrets.choice(charset) for _ in range(length))

def main(argv=None):
    parser = argparse.ArgumentParser(description="Secure password generator")
    parser.add_argument('-l', '--length', type=int, default=16, help='Length of each password (default: 16)')
    parser.add_argument('-n', '--number', type=int, default=1, help='How many passwords to generate (default: 1)')
    parser.add_argument('--no-lower', action='store_true', help='Exclude lowercase letters')
    parser.add_argument('--no-upper', action='store_true', help='Exclude uppercase letters')
    parser.add_argument('--no-digits', action='store_true', help='Exclude digits')
    parser.add_argument('--no-symbols', action='store_true', help='Exclude symbols')
    parser.add_argument('--avoid-ambiguous', action='store_true', help='Avoid ambiguous characters like 0/O, l/1')
    parser.add_argument('--copy', action='store_true', help='Copy the first generated password to clipboard (requires pyperclip)')
    args = parser.parse_args(argv)

    try:
        charset = build_charset(
            use_lower=not args.no_lower,
            use_upper=not args.no_upper,
            use_digits=not args.no_digits,
            use_symbols=not args.no_symbols,
            avoid_ambiguous=args.avoid_ambiguous
        )
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        parser.print_help()
        sys.exit(2)

    if args.length <= 0:
        print("Error: length must be positive integer", file=sys.stderr)
        sys.exit(2)
    if args.number <= 0:
        print("Error: number must be positive integer", file=sys.stderr)
        sys.exit(2)

    passwords = [generate_password(args.length, charset) for _ in range(args.number)]
    for i, p in enumerate(passwords, start=1):
        if args.number == 1:
            print(p)
        else:
            print(f"{i}: {p}")

    if args.copy:
        if not PYPERCLIP_AVAILABLE:
            print("pyperclip not installed — cannot copy to clipboard. Install with: pip install pyperclip", file=sys.stderr)
        else:
            pyperclip.copy(passwords[0])
            print("First password copied to clipboard.")

if __name__ == '__main__':
    main()
