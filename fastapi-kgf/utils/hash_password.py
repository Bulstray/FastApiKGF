import bcrypt


def hash_password_simple(password: str) -> bytes:
    password_bytes = password.encode('utf-8')

    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)

    return hashed