import os
from dotenv import load_dotenv, find_dotenv
import jwt


async def validate_token_async(db, auth_token):
    load_dotenv(find_dotenv())
    try:
        payload = jwt.decode(
            auth_token,
            os.environ.get("TOKEN_SECRET"),
            verify=True,
            algorithms=["HS256"],
        )
        await db.connect()
        blocklisted_token = await db.tokenblocklist.find_unique(
            where={"expired_token": auth_token}
        )
        await db.disconnect()
        if blocklisted_token:
            raise Exception("Token previously used")
        return payload
    except Exception as e:
        print(e)
        return False
