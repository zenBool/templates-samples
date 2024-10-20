import inspect

from loguru import logger
import logging

# Переменная для установки уровня логирования
# или "DEBUG", "INFO", "WARNING", "ERROR" и т.д.
log_level = logging.INFO


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists.
        level: str | int
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def configure_logging(level: int = log_level):
    logging.basicConfig(
        handlers=[InterceptHandler()],
        level=level,
        force=True,
        # format="%(funcName)20s %(module)s:%(lineno)d %(levelname)-8s - %(message)s",
        format="[%(asctime)s.%(msecs)03d] %(funcName)20s %(module)s:%(lineno)d %(levelname)-8s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
