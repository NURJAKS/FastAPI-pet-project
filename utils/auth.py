import bcrypt

def hash_password(password: str) -> str:
    """Хешируем пароль для хранения в БД."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    """Проверяем введённый пароль с хешем."""
    return bcrypt.checkpw(password.encode(), hashed.encode())
