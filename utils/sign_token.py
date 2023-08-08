import os, datetime
import pytz
from dotenv import load_dotenv, find_dotenv
import jwt


def sign_token(user):
    load_dotenv(find_dotenv())
    return jwt.encode(
        {
            "id": user.id,
            "name": user.name,
            "isAdmin": user.is_admin,
            "iat": datetime.datetime.now(tz=pytz.timezone("Asia/Tel_Aviv")),
            "exp": datetime.datetime.now(tz=pytz.timezone("Asia/Tel_Aviv"))
            + datetime.timedelta(days=7),
        },
        os.environ.get("TOKEN_SECRET"),
    )
