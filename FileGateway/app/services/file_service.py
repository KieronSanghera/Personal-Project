from fastapi import UploadFile

def get_metadata(file: UploadFile):
    metadata = {
        "filename": file.filename,
        "filesize": file.size
    }
    return metadata
