from domain.exceptions import UserAlreadyExistsError, UserNotFoundError
from domain.models import UserDomain, Role, UserSettings
from domain.uow import AbstractUnitOfWork


class UserService:
    def __init__(
        self,
        uow: AbstractUnitOfWork,
    ):
        self.__user_repo = uow.user_repo

    async def exists(self, id: int) -> bool:
        """
        Проверяет, существует ли пользователь.

        :param id: ID пользователя.
        :return: True, если пользователь существует, иначе False.
        """
        return await self.__user_repo.exists(id)

    async def create_user(
        self,
        *,
        id: int,
        username: str,
        password: str,
        role: Role,
        name: str,
        check_valid_fields: bool = False,
    ) -> UserDomain:
        """
        Создает нового пользователя, проверяет валидность полей и их уникальность.

        :param id: Идентификатор пользователя.
        :param username: Username пользователя.
        :param password: Нехешированный пароль пользователя.
        :param role: Роль пользователя.
        :param name: Имя пользователя.
        :param check_valid_fields: Проверять ли валидность полей.
        :return: Доменная модель пользователя.
        :raise UserAlreadyExistsError: Если пользователь с таким именем или username уже существует.
        :raise ValidationError: Если пароль, имя или username невалидны.
        """
        if check_valid_fields:
            UserSettings.validate_password(password)
            UserSettings.validate_name(name)
            UserSettings.validate_username(username)

        if await self.__user_repo.get_by_username(username) is not None:
            raise UserAlreadyExistsError(username=username)

        if await self.__user_repo.get_by_name(name) is not None:
            raise UserAlreadyExistsError(name=name)

        password = UserSettings.hash_password(password)
        user = await self.__user_repo.create(
            id=id,
            name=name,
            username=username,
            password=password,
            role=role,
        )
        return user

    async def get_user_by_id(self, id: int) -> UserDomain:
        """
        Возвращает пользователя по его id.

        :param id: ID пользователя.
        :return: Доменная модель пользователя.
        :raise UserNotFoundError: Если пользователь не найден.
        """
        user = await self.__user_repo.get_by_id(id)
        if user is None:
            raise UserNotFoundError(id=id)
        return user

    async def get_user_by_name(self, name: str) -> UserDomain:
        """
        Возвращает пользователя по его имени.

        :param name: Имя пользователя.
        :return: Доменная модель пользователя.
        :raise UserNotFoundError: Если пользователь не найден.
        """
        user = await self.__user_repo.get_by_name(name)
        if user is None:
            raise UserNotFoundError(name=name)
        return user

    async def get_user_by_username(self, username: str) -> UserDomain:
        """
        Возвращает пользователя по его username.

        :param username: Username пользователя.
        :return: Доменная модель пользователя.
        :raise UserNotFoundError: Если пользователь не найден.
        """
        user = await self.__user_repo.get_by_username(username)
        if user is None:
            raise UserNotFoundError(username=username)
        return user

    async def update_user(
        self,
        user_id: int,
        *,
        name: str | None = None,
        username: str | None = None,
        password: str | None = None,
        role: Role | None = None,
    ) -> UserDomain:
        """
        Обновляет пользователя, проверяет валидность полей,
        уникальность username и name, хеширует пароль и обновляет пользователя.


        :param user_id: ID пользователя.
        :param name: Имя пользователя.
        :param username: Username пользователя.
        :param password: Пароль пользователя.
        :param role: Роль пользователя.
        :return: Обновленный объект пользователя.
        :raise UserAlreadyExistsError: Если пользователь с таким именем или username уже существует.
        :raise ValidationError: Если пароль, имя или username невалидны.
        """
        user = await self.get_user_by_id(user_id)

        if name is None and username is None and password is None and role is None:
            return user

        if name is not None and name != user.name:
            user_by_name = await self.__user_repo.get_by_name(name)
            if user_by_name is not None:
                raise UserAlreadyExistsError(name=name)
            UserSettings.validate_name(name)

        if username is not None and username != user.username:
            user_by_username = await self.__user_repo.get_by_username(username)
            if user_by_username is not None:
                raise UserAlreadyExistsError(username=username)
            UserSettings.validate_username(username)

        if password is not None:
            UserSettings.validate_password(password)
            password = UserSettings.hash_password(password)

        updated = await self.__user_repo.update(
            user_id,
            name=name,
            username=username,
            password=password,
            role=role,
        )
        assert updated
        return updated

    async def delete_user(self, user_id: int) -> UserDomain:
        """
        Удаляет пользователя.

        :param user_id: ID пользователя.
        :return: Удалённый объект пользователя.
        :raise UserNotFoundError: Если пользователь не найден.
        """
        deleted = await self.__user_repo.delete(user_id)
        if deleted is None:
            raise UserNotFoundError(id=user_id)
        return deleted

    async def list_users(self, by_role: Role | None = None) -> list[UserDomain]:
        """
        Возвращает список пользователей.

        :param by_role: Роль пользователя.
        :return: Список доменных моделей пользователей.
        """
        return await self.__user_repo.get_all(by_role=by_role)
