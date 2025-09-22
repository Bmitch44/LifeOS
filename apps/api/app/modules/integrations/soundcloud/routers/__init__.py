from .auth_router import router as soundcloud_auth_router
from .me_router import router as soundcloud_me_router

__all__ = [
    "soundcloud_auth_router",
    "soundcloud_me_router",
]

