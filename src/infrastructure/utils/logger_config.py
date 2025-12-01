import contextvars
import uuid
from typing import Literal

from loguru import logger

trace_id_var = contextvars.ContextVar("trace_id", default=None)


class LoggerConfig:
    @staticmethod
    def setup(level: Literal["DEBUG", "INFO", "ERROR"] = "INFO"):
        logger.remove()

        # Добавляем уровень PROFILE, если он ещё не существует
        if "PROFILE" not in [lvl.name for lvl in logger._core.levels.values()]:  # type: ignore
            logger.level("PROFILE", no=10, color="<blue>")

        def profile(self, message, *args, **kwargs):
            self.log("PROFILE", message, *args, **kwargs)

        setattr(logger.__class__, "profile", profile)

        logger.add(
            sink=lambda msg: print(msg, end=""),
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "[{extra[trace_id]}] - "
            "{message}",
            level=level,
        )
        return logger

    @staticmethod
    def set_trace_id(trace_id=None):
        if trace_id is None:
            trace_id = str(uuid.uuid4())
        trace_id_var.set(trace_id)  # type: ignore
        return trace_id

    @staticmethod
    def get_logger():
        trace = trace_id_var.get() or "no-trace"
        return logger.bind(trace_id=trace)


class TraceLoggerProxy:
    def __getattr__(self, name):
        trace = trace_id_var.get() or "no-trace"
        return getattr(logger.bind(trace_id=trace), name)


LoggerConfig.setup()
log = TraceLoggerProxy()
