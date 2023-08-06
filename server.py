import os, datetime
import asyncio
from operator import itemgetter
from flask import Flask, request, Response, Blueprint
from flask_cors import CORS, cross_origin
from prisma import Prisma
from dotenv import load_dotenv, find_dotenv
import bcrypt
import jwt

app = Flask(__name__)
cors = CORS(app)

loop = asyncio.get_event_loop()

db = Prisma()

load_dotenv(find_dotenv())


def sign_token(user):
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


async def login_async(email, password):
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


async def register_async(name, email, password):
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


async def check_if_existing_user_async(email):
    await db.connect()
    existing_user = await db.user.find_first(where={"email": email})
    await db.disconnect()
    if existing_user:
        return True
    else:
        return False


bp = Blueprint("api", __name__, url_prefix="/api")


@bp.route("/check-if-existing-user", methods=["POST"])
@cross_origin()
def check_if_existing_user():
    try:
        user_exists = loop.run_until_complete(
            check_if_existing_user_async(request.json["email"])
        )
        if user_exists:
            return Response(
                "An account for this email address already exists. Please log in.",
                status=400,
            )
        else:
            return "OK"
    except Exception as e:
        print(e)
        return Response(
            "Sorry, there was a problem signing you up. Please try again later.",
            status=400,
        )


@bp.route("/login", methods=["POST"])
@cross_origin()
def login():
    email, password = itemgetter("email", "password")(request.json)
    try:
        login_payload = loop.run_until_complete(login_async(email, password))
        if login_payload:
            return login_payload
        else:
            raise Exception("Invalid credentials")
    except Exception as e:
        print(e)
        return Response(
            "The email address and password you entered do not match",
            status=400,
        )


@bp.route("/register", methods=["POST"])
@cross_origin()
def register():
    name, email, password = itemgetter("name", "email", "password")(request.json)
    try:
        signup_payload = loop.run_until_complete(register_async(name, email, password))
        if signup_payload:
            return signup_payload
        else:
            raise Exception("Error adding new user to database.")
    except Exception as e:
        print(e)
        return Response(
            "Sorry, there was a problem signing you up. Please try again later.",
            status=400,
        )


app.register_blueprint(bp)
