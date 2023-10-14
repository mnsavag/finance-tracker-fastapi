import bcrypt


def get_password_hash(plain_password: str | bytes) -> str:
    if isinstance(plain_password, str):
        plain_password = plain_password.encode()

    return bcrypt.hashpw(plain_password, bcrypt.gensalt()).decode()
