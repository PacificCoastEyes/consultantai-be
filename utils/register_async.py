from .sign_token import sign_token
import bcrypt


async def register_async(db, name, email, password):
    await db.connect()
    encrypted_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    new_user = await db.user.create(
        {
            "name": name,
            "email": email,
            "password": encrypted_password.decode("utf-8"),
            "is_admin": False,
        }
    )
    await db.disconnect()
    if new_user:
        auth_token = sign_token(new_user)
        return {
            "authToken": auth_token,
            "firstName": new_user.name.split(" ")[0],
            "isAdmin": new_user.is_admin,
        }
    else:
        return None
