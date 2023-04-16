import os
from datetime import datetime, timedelta
from flask.blueprints import Blueprint
from .lib.auth import login_required
from flask import jsonify

Runtime = Blueprint("runtime", __name__, url_prefix="/api/runtime")

runtime = {
    "status": "stopped",  # running, stopped
    "since": datetime.now(),
    "duration": str(timedelta(seconds=1))
}


@Runtime.route("/list", methods=["POST"])
@login_required
def listRuntime():
    runtime["duration"] = str(datetime.now() - runtime["since"]).split(".")[0]
    return jsonify({
        "code": 200,
        "status": runtime["status"],
        "since": runtime["since"],
        "duration": runtime["duration"]
    })


@Runtime.route("/start", methods=["POST"])
@login_required
def startRuntime():
    if runtime["status"] == "stopped":
        os.system("nohup python chatgptscan.py automatic_scan --threads 20 > log &")
        runtime["status"] = "running"
        runtime["since"] = datetime.now()
        return jsonify({"code": 200})
    else:
        return jsonify({"code": 403})


@Runtime.route("/stop", methods=["POST"])
@login_required
def stopRuntime():
    os.system("ps aux | grep chatgptscan.py | awk '{print $2}' | xargs kill -9")
    runtime["status"] = "stopped"
    runtime["since"] = datetime.now()
    return jsonify({
        "code": 200
    })
