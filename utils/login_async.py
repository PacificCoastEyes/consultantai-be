from .sign_token import sign_token
import bcrypt


async def login_async(db, email, password):
    await db.connect()
    user = await db.user.find_first(where={"email": email})
    await db.disconnect()
    if user:
        passwords_match = bcrypt.checkpw(
            password.encode("utf-8"), user.password.encode("utf-8")
        )
        if passwords_match:
            auth_token = sign_token(user)
            return {
                "authToken": auth_token,
                "firstName": user.name.split(" ")[0],
                "isAdmin": user.is_admin,
            }
        else:
            return None
    else:
        return None
