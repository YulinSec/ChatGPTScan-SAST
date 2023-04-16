from flask import jsonify, request
from flask.blueprints import Blueprint
from api.lib.auth import login_required
from utils.mysql_utils import getScanResult

Scan = Blueprint("scan", __name__, url_prefix="/api/scan")


@Scan.route("/list", methods=["POST"])
@login_required
def listResult():
    page_size = int(request.json.get("page_size", 100))
    page_num = int(request.json.get("page_num", 1))
    project_name = request.json.get("project_name", "")
    filename = request.json.get("file_name", "")
    report = request.json.get("report", "")
    filename_not = request.json.get("file_name_not", "")
    report_not = request.json.get("report_not", "")
    data, queryScanResultCount = getScanResult(page_num, page_size, project_name, filename, report, filename_not, report_not)
    return jsonify({
        "code": 200,
        "data": data,
        "count": queryScanResultCount
    })
