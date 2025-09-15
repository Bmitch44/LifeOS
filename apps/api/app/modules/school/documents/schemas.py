from pydantic import BaseModel
from typing import List
from app.db.models import Document


class DocumentCreate(BaseModel):
    name: str
    description: str | None = None
    file_url: str
    file_type: str | None = None
    size: int | None = None


class DocumentUpdate(DocumentCreate):
    pass


class PaginatedDocuments(BaseModel):
    items: List[Document]
    page: int
    size: int
    total: int

