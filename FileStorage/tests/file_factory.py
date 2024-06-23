import factory
from factory import Faker

class FileFactory(factory.DictFactory):
    file_id=Faker("uuid4")
    filename=Faker("file_name")
    filesize=10