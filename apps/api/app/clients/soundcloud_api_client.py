import base64
import hashlib
import os
import time
from typing import Dict, Optional, Tuple, List

import requests
from fastapi import HTTPException

from app.settings import settings


class SoundCloudClient:
    """Thin HTTP client for SoundCloud API with OAuth2 Authorization Code + PKCE.

    This client focuses on HTTP operations and token handling only. Persistence and
    routing are handled at the service layer.
    """

    AUTH_BASE = "https://secure.soundcloud.com"
    API_BASE = "https://api.soundcloud.com"

    def __init__(self, clerk_user_id: Optional[str] = None) -> None:
        self.client_id = settings.soundcloud_client_id
        self.client_secret = settings.soundcloud_client_secret
        self.default_redirect_uri = settings.soundcloud_redirect_uri
        self.clerk_user_id = clerk_user_id

        if not self.client_id:
            raise ValueError("SoundCloud client_id is required. Set LIFEOS_SOUNDCLOUD_CLIENT_ID.")

    # PKCE helpers
    @staticmethod
    def _base64url(data: bytes) -> str:
        return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")

    @staticmethod
    def generate_code_verifier(length: int = 64) -> str:
        alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._~"
        rng = os.urandom
        # Generate with uniform selection from alphabet
        verifier_bytes = bytearray()
        while len(verifier_bytes) < length:
            # Take random byte, map to alphabet index
            for b in rng(32):
                idx = b % len(alphabet)
                verifier_bytes.append(ord(alphabet[idx]))
                if len(verifier_bytes) >= length:
                    break
        return verifier_bytes.decode("ascii")

    @staticmethod
    def generate_code_challenge(verifier: str) -> str:
        digest = hashlib.sha256(verifier.encode("ascii")).digest()
        return SoundCloudClient._base64url(digest)

    # OAuth flows
    def build_authorize_url(
        self,
        *,
        redirect_uri: Optional[str] = None,
        scope: str = "*",
        state: Optional[str] = None,
    ) -> Tuple[str, str, str]:
        """Return (authorize_url, code_verifier, state).

        The caller must store the returned code_verifier and state and provide them
        back to exchange_code_for_token.
        """
        code_verifier = self.generate_code_verifier()
        code_challenge = self.generate_code_challenge(code_verifier)
        if not state:
            state = self._base64url(os.urandom(24))
        redirect = redirect_uri or self.default_redirect_uri
        if not redirect:
            raise ValueError("redirect_uri is required (configure LIFEOS_SOUNDCLOUD_REDIRECT_URI or pass explicitly).")

        params = {
            "client_id": self.client_id,
            "redirect_uri": redirect,
            "response_type": "code",
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
            "state": state,
            "scope": scope,
        }
        query = "&".join(f"{k}={requests.utils.quote(str(v))}" for k, v in params.items())
        url = f"{self.AUTH_BASE}/authorize?{query}"
        return url, code_verifier, state

    def exchange_code_for_token(
        self,
        *,
        code: str,
        code_verifier: str,
        redirect_uri: Optional[str] = None,
    ) -> Dict:
        """Exchange authorization code for access and refresh tokens.

        Returns token dict augmented with expires_at.
        """
        redirect = redirect_uri or self.default_redirect_uri
        if not redirect:
            raise ValueError("redirect_uri is required to exchange code.")

        data = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "redirect_uri": redirect,
            "code_verifier": code_verifier,
            "code": code,
        }
        if self.client_secret:
            data["client_secret"] = self.client_secret

        try:
            resp = requests.post(f"{self.AUTH_BASE}/oauth/token", data=data, timeout=30)
            resp.raise_for_status()
            token = resp.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to exchange code: {e}") from e

        self._augment_token_expiry(token)
        return token

    def refresh_access_token(self, *, refresh_token: str) -> Dict:
        data = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "refresh_token": refresh_token,
        }
        if self.client_secret:
            data["client_secret"] = self.client_secret

        try:
            resp = requests.post(f"{self.AUTH_BASE}/oauth/token", data=data, timeout=30)
            resp.raise_for_status()
            token = resp.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to refresh token: {e}") from e

        self._augment_token_expiry(token)
        return token

    @staticmethod
    def _augment_token_expiry(token: Dict) -> None:
        expires_in = int(token.get("expires_in", 3600))
        token["expires_at"] = int(time.time()) + max(0, expires_in - 60)

    @staticmethod
    def is_token_expired(token: Dict) -> bool:
        return int(token.get("expires_at", 0)) <= int(time.time())

    # HTTP helpers
    @staticmethod
    def _auth_headers(token: Dict) -> Dict[str, str]:
        return {
            "accept": "application/json; charset=utf-8",
            "Authorization": f"Bearer {token.get('access_token')}",
        }

    def get(self, path: str, *, token: Dict, params: Optional[Dict] = None) -> Dict:
        try:
            resp = requests.get(f"{self.API_BASE}{path}", headers=self._auth_headers(token), params=params, timeout=30)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"GET {path} failed: {e}") from e

    def get_me(self, *, token: Dict) -> Dict:
        return self.get("/me", token=token)

    def get_liked_tracks(self, *, user_urn: str, token: Dict, limit: Optional[int] = None) -> List[Dict]:
        url = f"{self.API_BASE}/users/{user_urn}/likes/tracks"
        params = {"limit": 200, "linked_partitioning": 1}
        headers = self._auth_headers(token)

        tracks: List[Dict] = []
        next_href: Optional[str] = url
        try:
            while next_href:
                if next_href == url:
                    resp = requests.get(next_href, params=params, headers=headers, timeout=30)
                else:
                    resp = requests.get(next_href, headers=headers, timeout=30)
                resp.raise_for_status()
                data = resp.json()
                collection = data.get("collection", [])
                tracks.extend(collection)
                if limit and len(tracks) >= limit:
                    return tracks[:limit]
                next_href = data.get("next_href")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch liked tracks: {e}") from e

        return tracks

    def get_track_stream_url(self, *, track_id: int, token: Dict) -> Optional[str]:
        url = f"{self.API_BASE}/tracks/{track_id}/stream"
        headers = self._auth_headers(token)
        try:
            resp = requests.get(url, headers=headers, allow_redirects=False, timeout=30)
            if resp.status_code in (301, 302, 303, 307, 308):
                return resp.headers.get("Location")
            resp.raise_for_status()
            return None
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get stream url: {e}") from e

