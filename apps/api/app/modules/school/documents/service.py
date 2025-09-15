from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.school.documents.repo import DocumentsRepo
from app.modules.school.documents.schemas import DocumentCreate, PaginatedDocuments, DocumentUpdate
from app.db.models import Document


class DocumentsService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = DocumentsRepo(session)

    async def list_documents(self, page: int, size: int) -> PaginatedDocuments:
        return await self.repo.paginate(page, size)

    async def create_document(self, payload: DocumentCreate) -> Document:
        return await self.repo.create(payload)

    async def get_document(self, id: int) -> Document:
        return await self.repo.get(id)

    async def update_document(self, id: int, payload: DocumentUpdate) -> Document:
        return await self.repo.update(id, payload)

    async def delete_document(self, id: int) -> dict:
        return await self.repo.delete(id)

