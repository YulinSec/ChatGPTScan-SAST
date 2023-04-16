from flask import request,  jsonify, g
from flask.blueprints import Blueprint
from .lib.auth import login_required
from utils.mysql_utils import getUserByUsername, updatePasswordByUsername


User = Blueprint("user", __name__, url_prefix="/api/user")


@User.route("/password", methods=["POST"])
@login_required
def updatePassword():
    res = {"code": 403}
    oldPassword = request.json["oldPassword"]
    newPassword = request.json["newPassword"]
    username = g.data["username"]
    queryResult = getUserByUsername(username)
    if queryResult["success"]:
        user = queryResult["data"]
        if username == user["username"] and oldPassword == user["password"]:
            updatePasswordByUsername(username, newPassword)
            res = {"code": 200}
    return jsonify(res)
