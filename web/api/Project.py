from flask import jsonify, request
from flask.blueprints import Blueprint

from api.lib.auth import login_required
from utils.mysql_utils import getProjectSource

Project = Blueprint("project", __name__, url_prefix="/api/project")


@Project.route("/list", methods=["POST"])
@login_required 
def listProject():
    page_size = int(request.json.get("page_size", 100))
    page_num = int(request.json.get("page_num", 1))
    project_name = request.json.get("project_name", "")
    language = request.json.get("language", "")
    category = request.json.get("category", "")
    foundation = request.json.get("foundation", "")
    data, queryProjectSourceCount = getProjectSource(page_num, page_size,
                            project_name, language, category, foundation)
    return jsonify({
        "code": 200,
        "data": data,
        "count": queryProjectSourceCount
    })
