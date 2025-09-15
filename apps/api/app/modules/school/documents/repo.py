from fastapi import HTTPException
from app.modules.school.documents.schemas import DocumentCreate, PaginatedDocuments, DocumentUpdate
from app.db.models import Document
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func


class DocumentsRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def paginate(self, page: int, size: int) -> PaginatedDocuments:
        try:
            offset = (page - 1) * size
            total_query = select(func.count()).select_from(Document)
            total_result = await self.session.execute(total_query)
            total = total_result.scalar_one()
            query = select(Document).offset(offset).limit(size)
            result = await self.session.execute(query)
            items = result.scalars().all()
            return PaginatedDocuments(items=items, page=page, size=size, total=total)
        except Exception as e:
            await self.session.rollback()
            raise e

    async def create(self, payload: DocumentCreate) -> Document:
        try:
            doc = Document(
                name=payload.name,
                description=payload.description,
                file_url=payload.file_url,
                file_type=payload.file_type,
                size=payload.size,
            )
            self.session.add(doc)
            await self.session.commit()
            await self.session.refresh(doc)
            return doc
        except Exception as e:
            await self.session.rollback()
            raise e

    async def get(self, id: int) -> Document:
        try:
            doc = await self.session.get(Document, id)
            if not doc:
                raise HTTPException(status_code=404, detail="Document not found")
            return doc
        except Exception as e:
            await self.session.rollback()
            raise e

    async def update(self, id: int, payload: DocumentUpdate) -> Document:
        try:
            doc = await self.session.get(Document, id)
            if not doc:
                raise HTTPException(status_code=404, detail="Document not found")
            doc.name = payload.name
            doc.description = payload.description
            doc.file_url = payload.file_url
            doc.file_type = payload.file_type
            doc.size = payload.size
            await self.session.commit()
            await self.session.refresh(doc)
            return doc
        except Exception as e:
            await self.session.rollback()
            raise e

    async def delete(self, id: int) -> dict:
        try:
            doc = await self.session.get(Document, id)
            if not doc:
                raise HTTPException(status_code=404, detail="Document not found")
            await self.session.delete(doc)
            await self.session.commit()
            return {"message": "Document deleted successfully"}
        except Exception as e:
            await self.session.rollback()
            raise e

