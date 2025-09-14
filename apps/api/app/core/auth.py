from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, Optional

import jwt
from jwt import PyJWKClient

from app.settings import settings


@dataclass
class AuthenticatedUser:
    sub: str
    user_id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    raw: Dict[str, Any] | None = None


@lru_cache(maxsize=1)
def _jwks_client() -> Optional[PyJWKClient]:
    if not settings.clerk_jwks_url:
        return None
    return PyJWKClient(settings.clerk_jwks_url)


def verify_bearer_token(token: str) -> AuthenticatedUser:
    if not settings.clerk_jwks_url or not settings.clerk_issuer:
        # In dev, allow unsigned tokens if Clerk not configured
        payload = jwt.decode(token, options={"verify_signature": False, "verify_aud": False})
        return AuthenticatedUser(sub=str(payload.get("sub")), email=payload.get("email"), raw=payload)

    jwk_client = _jwks_client()
    if jwk_client is None:
        raise ValueError("JWKS client not configured")
    signing_key = jwk_client.get_signing_key_from_jwt(token)
    payload = jwt.decode(
        token,
        signing_key.key,
        algorithms=["RS256", "ES256"],
        options={"verify_aud": False},
        issuer=settings.clerk_issuer,
    )
    return AuthenticatedUser(
        sub=str(payload.get("sub")), 
        raw=payload,
        email=payload.get("primary_email"), 
        user_id=payload.get("user_id"),
        first_name=payload.get("first_name"),
        last_name=payload.get("last_name"),
        phone=payload.get("primary_phone"),
    )


