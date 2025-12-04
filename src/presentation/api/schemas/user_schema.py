from pydantic import BaseModel, Field, ValidationError, model_validator

from domain.models import UserDomain, UserSettings, Role


class UserResponse(BaseModel):
    id: int = Field(description="Уникальный индефикатор пользователя", examples=[1])
    name: str = Field(
        description="Имя пользователя",
        min_length=UserSettings.NAME_MIN_LENGTH,
        max_length=UserSettings.NAME_MAX_LENGTH,
        examples=["John Doe"],
    )
    username: str = Field(
        description="Логин пользователя",
        min_length=UserSettings.NAME_MIN_LENGTH,
        max_length=UserSettings.NAME_MAX_LENGTH,
        examples=["johndoe"],
    )
    role: str = Field(description="Роль пользователя", examples=[Role.ADMIN.value])

    @classmethod
    def from_domain(cls, user: UserDomain) -> "UserResponse":
        return cls(
            id=user.id,
            name=user.name,
            username=user.username,
            role=user.role,
        )


class ListUsersResponse(BaseModel):
    users: list[UserResponse] = Field(..., description="Список пользователей")
    total: int = Field(..., description="Кол-во пользователей")

    @classmethod
    def from_domain(cls, users: list[UserDomain]) -> "ListUsersResponse":
        return cls(
            users=[UserResponse.from_domain(user) for user in users], total=len(users)
        )


class CreateUserRequest(BaseModel):
    id: int = Field(description="Уникальный индефикатор пользователя", examples=[1])
    name: str = Field(
        ...,
        min_length=UserSettings.NAME_MIN_LENGTH,
        max_length=UserSettings.NAME_MAX_LENGTH,
        description="Имя пользователя",
        examples=["John Doe"],
    )
    username: str = Field(
        ...,
        min_length=UserSettings.USERNAME_MIN_LENGTH,
        max_length=UserSettings.USERNAME_MAX_LENGTH,
        description="Логин пользователя",
        examples=["admin", "manager"],
    )
    role: Role = Field(
        ..., description="Роль пользователя", examples=[Role.MANAGER.value]
    )
    password: str = Field(
        ...,
        min_length=UserSettings.PASSWORD_MIN_LENGTH,
        max_length=UserSettings.PASSWORD_MAX_LENGTH,
        description="Пароль пользователя",
        examples=["root", "password"],
    )


class UpdateUserRequest(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=UserSettings.NAME_MIN_LENGTH,
        max_length=UserSettings.NAME_MAX_LENGTH,
        description="Имя пользователя",
    )
    username: str | None = Field(
        default=None,
        min_length=UserSettings.USERNAME_MIN_LENGTH,
        max_length=UserSettings.USERNAME_MAX_LENGTH,
        description="Логин пользователя",
    )
    password: str | None = Field(
        default=None,
        min_length=UserSettings.PASSWORD_MIN_LENGTH,
        max_length=UserSettings.PASSWORD_MAX_LENGTH,
        description="Пароль пользователя",
    )
    role: str | None = Field(default=Role.USER.value, description="Роль пользователя")

    @model_validator(mode="after")
    def validate_params(self, values):
        if (
            self.name is None
            and self.username is None
            and self.password is None
            and self.role is None
        ):
            raise ValidationError(
                "At least one of name, username, or password must be provided"
            )
        return self
