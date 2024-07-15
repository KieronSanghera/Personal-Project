from app import config
import os
from importlib import reload
from unittest.mock import patch, MagicMock


class TestConfigSuccess:

    def test_log_level_int(self):
        os.environ["LOG_LEVEL"] = "10"
        reload(config)
        assert config.EnvConfig().log_level == "10"

    def test_log_level_str(self):
        os.environ["LOG_LEVEL"] = "debug"
        reload(config)
        assert config.EnvConfig().log_level == "debug"
        assert config.EnvConfig().is_debug == True


class TestConfigFailure:

    def test_log_level_str_VALUEERROR(self):
        os.environ["LOG_LEVEL"] = "bread"
        assert config.EnvConfig().log_level == 20
