from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str

class UploadUrlRequest(BaseModel):
    content_type: str
    filename: str
