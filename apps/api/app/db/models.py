"""Aggregate import-only module to ensure models are imported for metadata.

Keep this file small: only import models from feature modules so that
`SQLModel.metadata` has all tables when initializing.
"""

from app.modules.users.models import User  # noqa: F401
from app.modules.school.assesments.models import Assesment  # noqa: F401
from app.modules.school.courses.models import Course  # noqa: F401
from app.modules.school.documents.models import Document  # noqa: F401
