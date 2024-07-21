from app.schemas.schemas import FileInformation, CommonEventFormat
from file_factory import FileInformationFactory
from cef_factory import CommonEventFormatFactory
from freezegun import freeze_time
from datetime import datetime


class TestSchemas:

    def test_file_information_as_form(self):
        file_info: FileInformation = FileInformationFactory.create()
        file_info_as_form: FileInformation = FileInformation.as_form(
            **file_info.model_dump()
        )
        assert file_info == file_info_as_form

    @freeze_time("2000-01-01 12:00:00")
    def test_common_event_format(self, caplog):
        expected_log = "CEF:1|Project|MetadataStorage|1.0.0|L0|No Event|0|2000-01-01 12:00:00|conn_id=Not set|file_id=Not set|pytest=Pytest logging functionality"
        log: CommonEventFormat = CommonEventFormatFactory.create()
        log.timestamp = datetime.now()
        log.extension["pytest"] = "Pytest logging functionality"
        log.log()
        assert expected_log in caplog.text
