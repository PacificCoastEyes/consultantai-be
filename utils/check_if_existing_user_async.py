async def check_if_existing_user_async(db, email):
    await db.connect()
    existing_user = await db.user.find_first(where={"email": email})
    await db.disconnect()
    if existing_user:
        return True
    else:
        return False
