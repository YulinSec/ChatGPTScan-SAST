import functools

from flask import request, current_app, g
from flask_restx import abort
from loguru import logger

from utils.auth_util import validate_token


def login_required(func):
    """
    登录权限装饰器
    需要正常登录
    """
    @functools.wraps(func)
    def inner(*args, **kwargs):
        token = request.headers.get("X-Token", None)
        ip = request.headers.get("X-Real-Ip", "")
        if token is not None:
            try:
                res = validate_token(token=token, current_app=current_app)
                if res["success"]:
                    g.data = res["data"]
                    logger.info(f"[request-log] ip: {ip} url: {request.url}")
                    return func(*args, **kwargs)
            except Exception:
                pass
        logger.info(f"[unAuth] ip: {ip} url: {request.url}")
        abort(404)

    return inner
