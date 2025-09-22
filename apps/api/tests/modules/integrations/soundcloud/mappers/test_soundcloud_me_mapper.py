import pytest

from app.modules.integrations.soundcloud.mappers.soundcloud_me_mapper import SoundcloudMeMapper


@pytest.mark.anyio
async def test_map_api_me_to_soundcloud_me():
    mapper = SoundcloudMeMapper("test_user")
    api_me = {
        "urn": "soundcloud:users:1",
        "avatar_url": "http://avatar",
        "city": "City",
        "country": "Country",
        "description": "Desc",
        "first_name": "First",
        "followers_count": 1,
        "following_count": 2,
        "full_name": "Full Name",
        "last_name": "Last",
        "likes_count": 3,
        "permalink": "me",
        "permalink_url": "http://sc/me",
        "plan": "free",
        "playlist_count": 0,
        "private_playlists_count": 0,
        "private_tracks_count": 0,
        "public_favorites_count": 0,
        "reposts_count": 0,
        "track_count": 0,
        "username": "user",
        "website": "http://site",
        "website_title": "site",
    }
    payload = mapper.map_api_me_to_soundcloud_me(api_me)
    assert payload.clerk_user_id == "test_user"
    assert payload.username == "user"


