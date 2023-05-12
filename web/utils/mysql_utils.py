from datetime import datetime
from typing import Tuple, List, Any
from sqlalchemy import and_
from utils.mysql_connector import mysql_session
from model.tables import project_source, scan_result, user, key_repo


@mysql_session
def mark_project_scanned(project_name, session):
    session.query(project_source).filter_by(project_name=project_name).update(
        {project_source.last_scan: datetime.now()})
    session.commit()


@mysql_session
def mark_project_updated(project_name, session):
    session.query(project_source).filter_by(project_name=project_name).update(
        {project_source.last_scan: datetime.now()})
    session.commit()


@mysql_session
def add_scan_result(project_id: int, filename: str, report: str, create_time: datetime, session):
    one_scan_result = scan_result(
        project_id=project_id,
        filename=filename,
        report=report,
        create_time=datetime.now()
    )
    session.add(one_scan_result)
    session.commit()


@mysql_session
def getAllKey(session) -> list:
    queryKeyList = session.query(key_repo).all()
    keyList = []
    for queryKey in queryKeyList:
        keyList.append(queryKey.key)
    return keyList


def format_record(record) -> dict:
    return {
        "id": record.id,
        "project_name": record.project_name,
        "repo_link": record.repo_link,
        "language": record.language.split(","),
        "category": record.category,
        "foundation": record.foundation,
        "last_update": record.last_update,
        "last_scan": record.last_scan
    }


@mysql_session
def mark_project_scanned(project_name, session):
    session.query(project_source).filter_by(project_name=project_name).update(
        {project_source.last_scan: datetime.now()})
    session.commit()


@mysql_session
def mark_project_updated(project_name, session):
    session.query(project_source).filter_by(project_name=project_name).update(
        {project_source.last_scan: datetime.now()})
    session.commit()


@mysql_session
def getUserByUsername(username: str, session) -> dict:
    res = {"success": False}
    queryUser = session.query(user).filter_by(username=username).first()
    if queryUser is not None:
        res["success"] = True
        res["data"] = queryUser.get_dict()
    return res


@mysql_session
def updatePasswordByUsername(username: str, password: str, session):
    session.query(user).filter_by(username=username).update({user.password: password})
    session.commit()


@mysql_session
def getProjectSource(page_num: int, page_size: int, project_name: int, language: int, category: int, foundation: int,
                     session) -> \
        Tuple[List[Any], Any]:
    queryProjectSourceList = session.query(project_source).filter(
        and_(
            project_source.project_name.like(f'%{project_name}%'),
            project_source.language.like(f'%{language}%'),
            project_source.category.like(f'%{category}%'),
            project_source.foundation.like(f'%{foundation}%')
        )
    ).offset((page_num - 1) * page_size).limit(page_size).all()
    queryProjectSourceCount = session.query(project_source).filter(
        and_(
            project_source.project_name.like(f'%{project_name}%'),
            project_source.language.like(f'%{language}%'),
            project_source.category.like(f'%{category}%'),
            project_source.foundation.like(f'%{foundation}%')
        )
    ).count()
    data = []
    for queryProjectSource in queryProjectSourceList:
        data.append(queryProjectSource.get_dict())
    return data, queryProjectSourceCount


@mysql_session
def getScanResult(page_num, page_size, project_name, filename, report, filename_not, report_not, session) -> Tuple[
    List[Any], Any]:
    if len(filename_not) == 0:
        if len(report_not) == 0:
            queryScanResultList = session.query(scan_result) \
                .join(project_source) \
                .filter(
                and_(
                    scan_result.filename.like(f'%{filename}%'),
                    scan_result.report.like(f'%{report}%'),
                    project_source.project_name.like(f'%{project_name}%')
                )
            ).offset((page_num - 1) * page_size).limit(page_size)
            queryScanResultCount = session.query(scan_result) \
                .join(project_source) \
                .filter(
                and_(
                    scan_result.filename.like(f'%{filename}%'),
                    scan_result.report.like(f'%{report}%'),
                    project_source.project_name.like(f'%{project_name}%')
                )
            ).count()
        else:
            queryScanResultList = session.query(scan_result) \
                .join(project_source) \
                .filter(
                and_(
                    scan_result.filename.like(f'%{filename}%'),
                    scan_result.report.like(f'%{report}%'),
                    scan_result.report.not_like(f'%{report_not}%'),
                    project_source.project_name.like(f'%{project_name}%')
                )
            ).offset((page_num - 1) * page_size).limit(page_size)
            queryScanResultCount = session.query(scan_result) \
                .join(project_source) \
                .filter(
                and_(
                    scan_result.filename.like(f'%{filename}%'),
                    scan_result.report.like(f'%{report}%'),
                    scan_result.report.not_like(f'%{report_not}%'),
                    project_source.project_name.like(f'%{project_name}%')
                )
            ).count()
    else:
        if len(report_not) == 0:
            queryScanResultList = session.query(scan_result) \
                .join(project_source) \
                .filter(
                and_(
                    scan_result.filename.like(f'%{filename}%'),
                    scan_result.filename.not_like(f'%{filename_not}%'),
                    scan_result.report.like(f'%{report}%'),
                    project_source.project_name.like(f'%{project_name}%')
                )
            ).offset((page_num - 1) * page_size).limit(page_size)
            queryScanResultCount = session.query(scan_result) \
                .join(project_source) \
                .filter(
                and_(
                    scan_result.filename.like(f'%{filename}%'),
                    scan_result.filename.not_like(f'%{filename_not}%'),
                    scan_result.report.like(f'%{report}%'),
                    project_source.project_name.like(f'%{project_name}%')
                )
            ).count()
        else:
            queryScanResultList = session.query(scan_result) \
                .join(project_source) \
                .filter(
                and_(
                    scan_result.filename.like(f'%{filename}%'),
                    scan_result.filename.not_like(f'%{filename_not}%'),
                    scan_result.report.like(f'%{report}%'),
                    scan_result.report.not_like(f'%{report_not}%'),
                    project_source.project_name.like(f'%{project_name}%')
                )
            ).offset((page_num - 1) * page_size).limit(page_size)
            queryScanResultCount = session.query(scan_result) \
                .join(project_source) \
                .filter(
                and_(
                    scan_result.filename.like(f'%{filename}%'),
                    scan_result.filename.not_like(f'%{filename_not}%'),
                    scan_result.report.like(f'%{report}%'),
                    scan_result.report.not_like(f'%{report_not}%'),
                    project_source.project_name.like(f'%{project_name}%')
                )
            ).count()

    data = []
    for queryScanResult in queryScanResultList:
        temp_dict = queryScanResult.get_dict()
        if ".git" in temp_dict["repo_link"]:
            link = temp_dict["repo_link"].split(".git")[-1] + "/tree/master/" + temp_dict["file_name"]
        else:
            link = temp_dict["repo_link"] + "/tree/master/" + temp_dict["file_name"]
        temp_dict["url"] = link
        data.append(temp_dict)
    return data, queryScanResultCount


@mysql_session
def getAllKeyWithBalance(session) -> list:
    queryKeyList = session.query(key_repo).all()
    keyList = []
    for queryKey in queryKeyList:
        keyList.append({
            "id": queryKey.id,
            "secret": queryKey.key[:5] + "********************" + queryKey.key[-2:],
            "balance": "NotImplemented"
        })
    return keyList


@mysql_session
def addKey(key, session):
    new_key = key_repo(key=key)
    session.add(new_key)
    session.commit()


@mysql_session
def delKey(key_id, session):
    session.query(key_repo).filter_by(id=key_id).delete()
    session.commit()
