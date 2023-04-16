from flask import request, jsonify
from flask.blueprints import Blueprint
from flask import current_app
from utils.auth_util import create_token
from .lib.auth import login_required
from utils.mysql_utils import getUserByUsername


Index = Blueprint("index", __name__, url_prefix="/api/index")


@Index.route("/login", methods=["POST"])
def login():
    res = {"code": 403}
    username = request.json["username"]
    password = request.json["password"]
    queryResult = getUserByUsername(username)
    if queryResult["success"]:
        user = queryResult["data"]
        if username == user["username"] and password == user["password"]:
            token = create_token(user=user, current_app=current_app)
            res = {
                "name": username,
                "perm": ["list", "add", "update", "delete"],
                "group": ["admin"],
                "code": 200,
                "token": token
            }
    return jsonify(res)


@Index.route("/index", methods=["GET", "POST"])
@login_required
def index():
    return "ok"
