from fastapi import UploadFile
import factory
from io import BytesIO
from app.schemas.schemas import FileInformation
from factory import Faker

class UploadFileFactory(factory.Factory):
    class Meta:
        model = UploadFile

    filename = factory.Faker('file_name', extension='txt')
    size = 21
    
    @factory.lazy_attribute
    def file(self):
        # Create a BytesIO object with some test content
        content = b'This is test content'
        file_like = BytesIO(content)
        # SpooledTemporaryFile needs a mode that matches the intended use (e.g., 'rb' for reading bytes)
        return file_like
    
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
