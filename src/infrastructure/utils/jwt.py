import uuid
from datetime import datetime, timedelta

from jose import JWTError, jwt

from config import settings

__all__ = ["create_access_token", "create_refresh_token", "decode_token"]


def create_access_token(
    data: dict, key: str, expires_delta: timedelta | None = None
) -> str:
    """
    Создает JWT access-токен с заданным временем истечения.

    :param data: Данные (payload), которые будут зашифрованы в токен.
    :param expires_delta: Время жизни токена .
    :return: Закодированный JWT-токен (строка).
    """
    expire = datetime.now() + (
        expires_delta if expires_delta else settings.access_token_expire
    )
    data.update({"exp": expire})
    data.update({"token_type": "access"})
    data.update({"jti": str(uuid.uuid4())})
    encoded_jwt = jwt.encode(data, key, algorithm=settings.algorithm)
    return encoded_jwt


def create_refresh_token(
    data: dict, key: str, expires_delta: timedelta | None = None
) -> str:
    """
    Создает JWT refresh-токен с фиксированным временем истечения.

    :param data: Данные (payload), которые будут зашифрованы в токен.
    :return: Закодированный refresh-токен (строка).
    """
    expire = datetime.now() + (
        expires_delta if expires_delta else settings.refresh_token_expire
    )
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    to_encode.update({"token_type": "refresh"})
    to_encode.update({"jti": str(uuid.uuid4())})
    encoded_jwt = jwt.encode(to_encode, key, algorithm=settings.algorithm)
    return encoded_jwt


def decode_token(token: str, key: str, token_type: str = "access") -> dict:
    """
    Декодирует JWT access-токен и извлекает идентификатор пользователя.

    :param token: Закодированный JWT-токен (строка).
    :return: ID пользователя (строка).
    :raises HTTPException: Если токен истек или недействителен.
    """
    payload = jwt.decode(token, key, algorithms=[settings.algorithm])
    token_type_jwt = payload.get("token_type", None)
    if token_type_jwt is None or token_type != token_type_jwt:
        raise JWTError("Invalid token type")
    return payload
