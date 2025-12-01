from datetime import datetime
from enum import Enum
from passlib.context import CryptContext
from pydantic import Field, ValidationError

from .domain_model import DomainModel
from .role_model import Role

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserModel(DomainModel):
    name: str
    username: str
    password: str


class UserSettings:
    """
    Настройки пользователя.
    """

    USERNAME_MIN_LENGTH = 4
    USERNAME_MAX_LENGTH = 16
    PASSWORD_MIN_LENGTH = 4
    PASSWORD_MAX_LENGTH = 50
    NAME_MIN_LENGTH = 4
    NAME_MAX_LENGTH = 50

    @staticmethod
    def hash_password(unhashed_password: str) -> str:
        """
        Хеширует пароль.

        Args:
            unhashed_password: пароль

        Returns:
            str: хешированный пароль
        """
        return pwd_context.hash(unhashed_password)

    @staticmethod
    def validate_password(password: str):
        """
        Проверяет пароль.

        Args:
            password: пароль
        """
        if len(password) < UserSettings.PASSWORD_MIN_LENGTH:
            raise ValidationError("Password is too short")
        if len(password) > UserSettings.PASSWORD_MAX_LENGTH:
            raise ValidationError("Password is too long")

    @staticmethod
    def validate_username(username: str):
        """
        Проверяет username.

        Args:
            username: username
        """
        if len(username) < UserSettings.USERNAME_MIN_LENGTH:
            raise ValidationError("Username is too short")
        if len(username) > UserSettings.USERNAME_MAX_LENGTH:
            raise ValidationError("Username is too long")

    @staticmethod
    def validate_name(name: str):
        """
        Проверяет имя.

        Args:
            name: имя
        """
        if len(name) < UserSettings.NAME_MIN_LENGTH:
            raise ValidationError("Name is too short")
        if len(name) > UserSettings.NAME_MAX_LENGTH:
            raise ValidationError("Name is too long")


class UserDomain(DomainModel):
    id: int = Field(description="Уникальный идентификатор пользователя", examples=[1])
    name: str = Field(description="Имя пользователя", examples=["Ваня"])
    username: str = Field(
        description="Username, нужен для авторизации пользователя", examples=["johndoe"]
    )
    role: Role = Field(
        description="Роль, которой принадлежит пользователю", examples=[Role.ADMIN]
    )
    password: str = Field(exclude=True)
    created_at: datetime = Field(
        description="Время создания пользователя", examples=["2022-01-01T00:00:00"]
    )
