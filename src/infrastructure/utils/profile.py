import asyncio
from abc import ABCMeta
from functools import wraps
from time import perf_counter

from config import settings
from infrastructure.utils.logger_config import log


def profile_func(func):
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        if not settings.dev_mode:
            return await func(*args, **kwargs)

        start_time = perf_counter()
        result = await func(*args, **kwargs)
        process_time = (perf_counter() - start_time) * 1000

        # Если метод класса, args[0] это self — пропускаем его
        cls_name = args[0].__class__.__name__ + "." if args else ""

        # Пропускаем self в логировании
        args_repr = [repr(a) for a in args[1:]] if args else []
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        all_params = ", ".join(args_repr + kwargs_repr)

        log.profile(
            f"{cls_name}{func.__name__}({all_params}) | Time: {process_time:.2f}ms"
        )
        return result

    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        if not settings.dev_mode:
            return func(*args, **kwargs)

        start_time = perf_counter()
        result = func(*args, **kwargs)
        process_time = (perf_counter() - start_time) * 1000

        cls_name = args[0].__class__.__name__ + "." if args else ""

        args_repr = [repr(a) for a in args[1:]] if args else []
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        all_params = ", ".join(args_repr + kwargs_repr)

        log.profile(
            f"{cls_name}{func.__name__}({all_params}) | Time: {process_time:.2f}ms"
        )
        return result

    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper


class ProfileMeta(type):
    def __new__(cls, name, bases, dct):
        for attr_name, attr_value in dct.items():
            if callable(attr_value) and not attr_name.startswith("__"):
                dct[attr_name] = profile_func(attr_value)
        return super().__new__(cls, name, bases, dct)


class ProfileABCMeta(ProfileMeta, ABCMeta):
    pass
