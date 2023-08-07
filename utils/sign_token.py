import os, datetime
from dotenv import load_dotenv, find_dotenv
import jwt


def sign_token(user):
    load_dotenv(find_dotenv())
    return jwt.encode(
        {
            "id": user.id,
            "name": user.name,
            "isAdmin": user.is_admin,
            "iat": datetime.datetime.now(),
            "exp": datetime.datetime.now() + datetime.timedelta(days=7),
        },
        os.environ.get("TOKEN_SECRET"),
    )
