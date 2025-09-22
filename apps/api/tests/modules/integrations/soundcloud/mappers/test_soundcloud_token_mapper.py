import pytest

from app.modules.integrations.soundcloud.mappers.soundcloud_token_mapper import SoundcloudTokenMapper


@pytest.mark.anyio
async def test_map_api_token_to_soundcloud_token():
    mapper = SoundcloudTokenMapper("test_user")
    api_token = {
        "access_token": "a",
        "token_type": "bearer",
        "expires_in": 3600,
        "refresh_token": "r",
        "scope": "*",
        "expires_at": 123,
    }
    payload = mapper.map_api_token_to_soundcloud_token(api_token)
    assert payload.clerk_user_id == "test_user"
    assert payload.access_token == "a"


