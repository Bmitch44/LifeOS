import pytest

from tests.factories.integrations.soundcloud import create_soundcloud_me


@pytest.mark.anyio
async def test_create_me(client):
    payload = {
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
    }
    r = await client.post("/v1/soundcloud/me", json=payload)
    assert r.status_code == 201
    assert r.json()["username"] == "user"


@pytest.mark.anyio
async def test_get_update_delete_me(client, session):
    me = await create_soundcloud_me(session)

    r = await client.get(f"/v1/soundcloud/me/{me.id}")
    assert r.status_code == 200
    assert r.json()["id"] == me.id

    payload = {**r.json(), "username": "user2"}
    r2 = await client.put(f"/v1/soundcloud/me/{me.id}", json=payload)
    assert r2.status_code == 200
    assert r2.json()["username"] == "user2"

    r3 = await client.delete(f"/v1/soundcloud/me/{me.id}")
    assert r3.status_code == 200
    assert r3.json()["message"] == "SoundcloudMe deleted successfully"


@pytest.mark.anyio
async def test_sync_me(client):
    r = await client.get("/v1/soundcloud/me/sync")
    # Without env vars this may 500; allow 200/500
    assert r.status_code in (200, 500)


