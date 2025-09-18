from app.db.models import User


async def create_user(session, **overrides):
    u = User(
        clerk_user_id=overrides.get("clerk_user_id", "user_test"),
        email=overrides.get("email", "user@test.dev"),
        first_name=overrides.get("first_name", "Test"),
        last_name=overrides.get("last_name", "User"),
        phone=overrides.get("phone"),
    )
    session.add(u)
    await session.commit()
    await session.refresh(u)
    return u