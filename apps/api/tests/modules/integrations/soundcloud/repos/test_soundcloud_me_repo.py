import pytest

from app.modules.integrations.soundcloud.repos.me_repo import MeRepo
from tests.factories.integrations.soundcloud import create_soundcloud_me


@pytest.mark.anyio
async def test_create_get_update_delete(session):
    repo = MeRepo(session, clerk_user_id="test_user")
    created = await repo.create(type("Obj", (), {
        "clerk_user_id": "test_user",
        "urn": "u",
        "avatar_url": "a",
        "city": "c",
        "country": "co",
        "description": "d",
        "first_name": "f",
        "followers_count": 1,
        "following_count": 2,
        "full_name": "fn",
        "last_name": "l",
        "likes_count": 3,
        "permalink": "p",
        "permalink_url": "pu",
        "plan": "free",
        "playlist_count": 0,
        "private_playlists_count": 0,
        "private_tracks_count": 0,
        "public_favorites_count": 0,
        "reposts_count": 0,
        "track_count": 0,
        "username": "user",
        "website": "w",
        "website_title": "wt",
    })())
    assert created.id is not None

    got = await repo.get(created.id)
    assert got.id == created.id

    got2 = await repo.get_by_clerk_user_id()
    assert got2 is not None and got2.id == created.id

    updated = await repo.update(created.id, type("Obj", (), {
        "clerk_user_id": "test_user",
        "urn": "u2",
        "avatar_url": "a2",
        "city": "c2",
        "country": "co2",
        "description": "d2",
        "first_name": "f2",
        "followers_count": 10,
        "following_count": 20,
        "full_name": "fn2",
        "last_name": "l2",
        "likes_count": 30,
        "permalink": "p2",
        "permalink_url": "pu2",
        "plan": "pro",
        "playlist_count": 1,
        "private_playlists_count": 2,
        "private_tracks_count": 3,
        "public_favorites_count": 4,
        "reposts_count": 5,
        "track_count": 6,
        "username": "user2",
        "website": "w2",
        "website_title": "wt2",
    })())
    assert updated.username == "user2"

    res = await repo.delete(created.id)
    assert res["message"] == "SoundcloudMe deleted successfully"


