async def blocklist_token_async(db, auth_token):
    await db.connect()
    token_blocklisted = await db.tokenblocklist.create({"expired_token": auth_token})
    await db.disconnect()
    return await token_blocklisted
