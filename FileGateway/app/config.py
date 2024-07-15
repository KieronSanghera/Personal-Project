from pydantic import model_validator
from pydantic_settings import BaseSettings
from typing import Union
from typing_extensions import Self
import logging


class EnvConfig(BaseSettings):
    """Load and parse environment variables"""

    log_level: Union[int, str] = 20

    @property
    def is_debug(self):
        log_level = (
            self.log_level.lower()
            if isinstance(self.log_level, str)
            else self.log_level
        )
        return log_level in [10, "debug"]

    @model_validator(mode="after")
    def post_log_level(self) -> Self:
        config_log_level = logging.INFO

        if isinstance(self.log_level, int):
            config_log_level = self.log_level

        if isinstance(self.log_level, str):
            log_level_upper = self.log_level.upper()

            if log_level_upper in {
                "CONFIG",
                "ERROR",
                "WARNING",
                "INFO",
                "DEBUG",
                "NOTSET",
            }:
                config_log_level = log_level_upper
            else:
                try:
                    config_log_level = int(self.log_level)
                except ValueError as e:
                    logging.error(
                        f"Invalid LOG_LEVEL value, Defaulting to log level INFO - {e}"
                    )
                    self.log_level = config_log_level
        logging.getLogger().setLevel(config_log_level)


configs = EnvConfig()
for key, value in configs:
    logging.info(f"{key} set to {value}")