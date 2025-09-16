"""Aggregate import-only module to ensure models are imported for metadata.

Keep this file small: only import models from feature modules so that
`SQLModel.metadata` has all tables when initializing.
"""

from app.modules.users.models import User
from app.modules.school.assesments.models import Assesment
from app.modules.school.courses.models import Course
from app.modules.school.lectures.models import Lecture
from app.modules.integrations.plaid.models import PlaidItem
from app.modules.integrations.plaid.models import PlaidAccount
from app.modules.integrations.snaptrade.models import SnaptradeConnection
from app.modules.integrations.snaptrade.models import SnaptradeAccount

__all__ = [
    User.__name__,
    Assesment.__name__,
    Course.__name__,
    Lecture.__name__,
    PlaidItem.__name__,
    PlaidAccount.__name__,
    SnaptradeConnection.__name__,
    SnaptradeAccount.__name__,
]