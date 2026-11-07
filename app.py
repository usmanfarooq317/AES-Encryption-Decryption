"""
AES Encryption / Decryption Tool
--------------------------------
Fixed settings:
  * Algorithm : AES
  * Mode      : CBC
  * Key size  : 128 bits  (secret key = 16 characters)
  * IV size   : 128 bits  (initialization vector = 16 characters)
  * Padding   : PKCS5 / PKCS7
  * Encrypt output format : Hex
  * Decrypt input format  : Hex
"""

import binascii
import re

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

KEY_SIZE_BYTES = 16   # 128-bit key
IV_SIZE_BYTES = 16    # 128-bit IV
BLOCK_SIZE_BITS = 128


class AESInputError(ValueError):
    """Raised when user input is invalid."""


def _validate_key_iv(secret_key: str, iv: str) -> tuple[bytes, bytes]:
    key_bytes = (secret_key or "").encode("utf-8")
    iv_bytes = (iv or "").encode("utf-8")

    if len(key_bytes) != KEY_SIZE_BYTES:
        raise AESInputError(
            f"Secret Key must be exactly {KEY_SIZE_BYTES} characters (128 bits). "
            f"You entered {len(key_bytes)}."
        )
    if len(iv_bytes) != IV_SIZE_BYTES:
        raise AESInputError(
            f"Initialization Vector must be exactly {IV_SIZE_BYTES} characters (128 bits). "
            f"You entered {len(iv_bytes)}."
        )
    return key_bytes, iv_bytes


def aes_encrypt(plain_text: str, iv: str, secret_key: str) -> str:
    """AES-128-CBC encrypt, PKCS7 padding, return Hex."""
    if not plain_text:
        raise AESInputError("Please enter the text to encrypt.")
    key_bytes, iv_bytes = _validate_key_iv(secret_key, iv)

    padder = padding.PKCS7(BLOCK_SIZE_BITS).padder()
    padded = padder.update(plain_text.encode("utf-8")) + padder.finalize()

    encryptor = Cipher(algorithms.AES(key_bytes), modes.CBC(iv_bytes)).encryptor()
    cipher_bytes = encryptor.update(padded) + encryptor.finalize()

    return cipher_bytes.hex()


def aes_decrypt(hex_text: str, iv: str, secret_key: str) -> str:
    """AES-128-CBC decrypt Hex input, remove PKCS7 padding, return plain text."""
    if not hex_text or not hex_text.strip():
        raise AESInputError("Please enter the encrypted (Hex) text to decrypt.")
    key_bytes, iv_bytes = _validate_key_iv(secret_key, iv)

    cleaned = re.sub(r"\s+", "", hex_text)   # allow spaces / new lines
    try:
        cipher_bytes = binascii.unhexlify(cleaned)
    except (binascii.Error, ValueError):
        raise AESInputError(
            "Encrypted text is not valid Hex. It should contain only 0-9 and a-f "
            "characters, with an even length."
        )

    if len(cipher_bytes) == 0 or len(cipher_bytes) % 16 != 0:
        raise AESInputError(
            "Encrypted data length is invalid for AES (must be a multiple of 16 bytes / 32 hex characters)."
        )

    decryptor = Cipher(algorithms.AES(key_bytes), modes.CBC(iv_bytes)).decryptor()
    padded = decryptor.update(cipher_bytes) + decryptor.finalize()

    try:
        unpadder = padding.PKCS7(BLOCK_SIZE_BITS).unpadder()
        plain_bytes = unpadder.update(padded) + unpadder.finalize()
    except ValueError:
        raise AESInputError(
            "Decryption failed. The Secret Key or Initialization Vector is incorrect, "
            "or the encrypted text is corrupted."
        )

    try:
        return plain_bytes.decode("utf-8")
    except UnicodeDecodeError:
        raise AESInputError(
            "Decryption produced non-text data. Please check the Secret Key and Initialization Vector."
        )


@app.route("/")
def index():
    return render_template("index.html")


@app.post("/api/encrypt")
def api_encrypt():
    data = request.get_json(silent=True) or {}
    try:
        result = aes_encrypt(data.get("text", ""), data.get("iv", ""), data.get("key", ""))
        return jsonify(success=True, result=result)
    except AESInputError as e:
        return jsonify(success=False, error=str(e)), 400
    except Exception:
        return jsonify(success=False, error="Unexpected error during encryption."), 500


@app.post("/api/decrypt")
def api_decrypt():
    data = request.get_json(silent=True) or {}
    try:
        result = aes_decrypt(data.get("text", ""), data.get("iv", ""), data.get("key", ""))
        return jsonify(success=True, result=result)
    except AESInputError as e:
        return jsonify(success=False, error=str(e)), 400
    except Exception:
        return jsonify(success=False, error="Unexpected error during decryption."), 500


if __name__ == "__main__":
    # Use host="0.0.0.0" to make it reachable from other machines on your network
    app.run(host="127.0.0.1", port=5000, debug=False)