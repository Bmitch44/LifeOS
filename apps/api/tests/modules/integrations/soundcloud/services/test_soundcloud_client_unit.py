import pytest

from app.clients.soundcloud_api_client import SoundCloudClient


@pytest.mark.anyio
async def test_pkce_generation_monotonic(monkeypatch):
    # Ensure settings present
    from app.settings import settings
    monkeypatch.setattr(settings, "soundcloud_client_id", "cid")
    monkeypatch.setattr(settings, "soundcloud_redirect_uri", "http://localhost/cb")

    client = SoundCloudClient()
    v = client.generate_code_verifier()
    c = client.generate_code_challenge(v)
    assert isinstance(v, str) and len(v) >= 43
    assert isinstance(c, str)


