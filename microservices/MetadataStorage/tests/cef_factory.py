import factory
from app.schemas.schemas import CommonEventFormat

class CommonEventFormatFactory(factory.Factory):
    class Meta:
        model = CommonEventFormat
    
    version = "1.0.0"
    