import logging

from typing import Any

logger = logging.getLogger('RAG')
logger.setLevel(logging.INFO)

log_format = '%(asctime)s (%(name)s) %(levelname)s: %(message)s'
logging.basicConfig(format=log_format)


class Logger:

    @staticmethod
    def info(message: Any) -> None:
        logger.info(message)

    @staticmethod
    def warning(message: Any) -> None:
        logger.warning(message)

    @staticmethod
    def error(message: Any) -> None:
        logger.error(message)