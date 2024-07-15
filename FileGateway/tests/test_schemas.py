from app.schemas.schemas import FileInformation, CommonEventFormat
from cef_factory import CommonEventFormatFactory
from freezegun import freeze_time
from datetime import datetime
import logging


class TestSchemas:

    @freeze_time("2000-01-01 12:00:00")
    def test_common_event_format(self, caplog):
        expected_log = "CEF:1|Project|FileGateway|1.0.0|L0|No Event|0|2000-01-01 12:00:00|conn_id=Not set|file_id=Not set|pytest=Pytest logging functionality"
        log: CommonEventFormat = CommonEventFormatFactory.create()
        log.timestamp = datetime.now()
        log.extension["pytest"] = "Pytest logging functionality"
        log.log()
        
        assert expected_log in caplog.text

