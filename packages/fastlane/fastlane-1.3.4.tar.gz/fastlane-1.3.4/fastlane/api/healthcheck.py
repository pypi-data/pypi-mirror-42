# 3rd Party
from flask import Blueprint, current_app, jsonify

# Fastlane
from fastlane.models import db

bp = Blueprint(  # pylint: disable=invalid-name
    "healthcheck", __name__, url_prefix="/healthcheck"
)


@bp.route("/", methods=("GET",))
def healthcheck():
    status = {"redis": True, "mongo": True, "errors": []}
    try:
        res = current_app.redis.ping()

        if not res:
            raise RuntimeError(f"Connection to redis failed ({res}).")
    except Exception as err:
        status["errors"].append({"source": "redis", "message": str(err)})
        status["redis"] = False

    try:
        database = current_app.config["MONGODB_SETTINGS"]["db"]
        conn = getattr(db.connection, database)
        res = tuple(conn.jobs.find().limit(1))

        if not isinstance(res, (tuple,)):
            raise RuntimeError(f"Connection to mongoDB failed ({res}).")
    except Exception as err:
        status["errors"].append({"source": "mongo", "message": str(err)})
        status["mongo"] = False

    code = 200

    if status["errors"]:
        code = 500

    return jsonify(status), code
