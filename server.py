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


bp = Blueprint("api", __name__, url_prefix="/api")


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
