import responses
from app.services.metadata_service import new_metadata_request
from app.schemas.schemas import FileInformation
from file_factory import FileInformationFactory


class TestMetadataServiceSuccess:
    
    @responses.activate  
    def test_metadata_service_successful(self):
        responses.add(
            method=responses.POST,
            url="http://localhost:80/newMetadata",
            status=201
        )
        fake_file_info: FileInformation = FileInformationFactory.create()
        stored = new_metadata_request(fake_file_info)
        assert stored == True
        
class TestMetadataServiceFail:
    
    @responses.activate  
    def test_metadata_service_successful(self):
        responses.add(
            method=responses.POST,
            url="http://localhost:80/newMetadata",
            status=500,
            body='{"detail": "pytest failure"}'
        )
        fake_file_info: FileInformation = FileInformationFactory.create()
        stored = new_metadata_request(fake_file_info)
        assert stored == False