from __future__ import annotations

import hashlib
import hmac
import os


PBKDF2_ALGORITHM = "sha256"
PBKDF2_ITERATIONS = 260000
SALT_BYTES = 16
HASH_BYTES = 32


def _encode_password_hash(salt: bytes, digest: bytes) -> str:
    return (
        f"pbkdf2_{PBKDF2_ALGORITHM}"
        f"${PBKDF2_ITERATIONS}"
        f"${salt.hex()}"
        f"${digest.hex()}"
    )


def _decode_password_hash(password_hash: str) -> tuple[int, bytes, bytes] | None:
    try:
        scheme, iterations, salt_hex, digest_hex = password_hash.split("$", 3)
        if scheme != f"pbkdf2_{PBKDF2_ALGORITHM}":
            return None

        iteration_count = int(iterations)
        salt = bytes.fromhex(salt_hex)
        digest = bytes.fromhex(digest_hex)
        if not salt or len(digest) != HASH_BYTES:
            return None
        return iteration_count, salt, digest
    except (TypeError, ValueError):
        return None


def hash_password(password: str) -> str:
    salt = os.urandom(SALT_BYTES)
    digest = hashlib.pbkdf2_hmac(
        PBKDF2_ALGORITHM,
        password.encode("utf-8"),
        salt,
        PBKDF2_ITERATIONS,
        dklen=HASH_BYTES,
    )
    return _encode_password_hash(salt=salt, digest=digest)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    parsed = _decode_password_hash(hashed_password)
    if not parsed:
        return False

    iterations, salt, stored_digest = parsed
    computed_digest = hashlib.pbkdf2_hmac(
        PBKDF2_ALGORITHM,
        plain_password.encode("utf-8"),
        salt,
        iterations,
        dklen=HASH_BYTES,
    )
    return hmac.compare_digest(computed_digest, stored_digest)
