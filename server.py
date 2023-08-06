import asyncio
from operator import itemgetter
from flask import Flask, request, Response, Blueprint
from flask_cors import CORS, cross_origin
from prisma import Prisma

app = Flask(__name__)
cors = CORS(app)

loop = asyncio.get_event_loop()

db = Prisma()


async def register_async(name, email, password):
    await db.connect()
    new_user = await db.user.create(
        {"name": name, "email": email, "password": password, "is_admin": False}
    )
    await db.disconnect()
    return new_user.id


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


@bp.route("/register", methods=["POST"])
@cross_origin()
def register():
    name, email, password = itemgetter("name", "email", "password")(request.json)
    try:
        return loop.run_until_complete(register_async(name, email, password))
    except Exception as e:
        print(e)
        return Response(
            "Sorry, there was a problem signing you up. Please try again later.",
            status=400,
        )


app.register_blueprint(bp)
