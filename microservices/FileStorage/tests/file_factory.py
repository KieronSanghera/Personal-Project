import factory
from factory import Faker
from app.schemas.schemas import FileInformation
from fastapi import UploadFile
from io import BytesIO


class FileInformationFactory(factory.Factory):
    class Meta:
        model = FileInformation

    file_id = Faker("uuid4")
    filename = Faker("file_name", extension="txt")
    filesize = 21

    @classmethod
    def create_dict(cls, **kwargs):
        """Return a dictionary representation of the factory's output."""
        obj = cls.create(**kwargs)
        return {key: str(value) for key, value in obj.__dict__.items()}


class UploadFileFactory(factory.Factory):
    class Meta:
        model = UploadFile

    file = BytesIO(b"test_data")
    size = 10
    filename = "pytest"
