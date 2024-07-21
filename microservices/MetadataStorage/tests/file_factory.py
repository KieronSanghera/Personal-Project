import factory
from factory import Faker
from app.schemas.schemas import FileInformation


class FileInformationFactory(factory.Factory):
    class Meta:
        model = FileInformation

    file_id = Faker("uuid4")
    filename = Faker("file_name", extension="txt")
    filesize = 21
    location = Faker("file_path")

    @classmethod
    def create_dict(cls, **kwargs):
        """Return a dictionary representation of the factory's output."""
        obj = cls.create(**kwargs)
        return {key: str(value) for key, value in obj.__dict__.items()}
