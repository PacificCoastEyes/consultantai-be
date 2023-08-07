import asyncio
from operator import itemgetter
from flask import Flask, request, Response, Blueprint
from flask_cors import CORS, cross_origin
from prisma import Prisma

from utils.login_async import login_async
from utils.register_async import register_async
from utils.check_if_existing_user_async import check_if_existing_user_async
from utils.blocklist_token_async import blocklist_token_async

app = Flask(__name__)
cors = CORS(app)

loop = asyncio.get_event_loop()

db = Prisma()


bp = Blueprint("api", __name__, url_prefix="/api")


@bp.route("/check-if-existing-user", methods=["POST"])
@cross_origin()
def check_if_existing_user():
    try:
        user_exists = loop.run_until_complete(
            check_if_existing_user_async(db, request.json["email"])
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
            status=500,
        )


@bp.route("/login", methods=["POST"])
@cross_origin()
def login():
    email, password = itemgetter("email", "password")(request.json)
    try:
        login_payload = loop.run_until_complete(login_async(db, email, password))
        if login_payload:
            return login_payload
        else:
            raise Exception("Invalid credentials")
    except Exception as e:
        print(e)
        return Response(
            "The email address and password you entered do not match.",
            status=400,
        )


@bp.route("/register", methods=["POST"])
@cross_origin()
def register():
    name, email, password = itemgetter("name", "email", "password")(request.json)
    try:
        signup_payload = loop.run_until_complete(
            register_async(db, name, email, password)
        )
        if signup_payload:
            return signup_payload
        else:
            raise Exception("Error adding new user to database.")
    except Exception as e:
        print(e)
        return Response(
            "Sorry, there was a problem signing you up. Please try again later.",
            status=500,
        )


@bp.route("/logout")
@cross_origin()
def logout():
    auth_token = request.headers["Authorization"].split(" ")[1]
    try:
        token_blocklisted = loop.run_until_complete(
            blocklist_token_async(db, auth_token)
        )
        if not token_blocklisted:
            raise Exception("Error adding token to database.")
    except Exception as e:
        print(e)
    finally:
        return "OK"


app.register_blueprint(bp)
