from flask.blueprints import Blueprint
from flask import jsonify, request
from .lib.auth import login_required
from utils.mysql_utils import getAllKey, addKey, delKey

Secret = Blueprint("secret", __name__, url_prefix="/api/secret")


@Secret.route("/list", methods=["POST"])
@login_required
def listSecret():
    allKey = getAllKey()
    return jsonify({
        "code": 200,
        "data": allKey
    })


@Secret.route("/add", methods=["POST"])
@login_required
def addSecret():
    res = {"code": 403}
    key = request.json.get("key", None)
    if key is not None:
        addKey(key)
        res["code"] = 200
    return jsonify(res)


@Secret.route("/del", methods=["POST"])
@login_required
def delSecret():
    key_id = request.json.get("id", "")
    delKey(key_id)
    return jsonify({
        "code": 200
    })
