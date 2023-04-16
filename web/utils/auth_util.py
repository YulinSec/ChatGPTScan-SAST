import time
import jwt
from jwt import ExpiredSignatureError


def create_token(user, current_app):
    headers = {
        "alg": "HS256",
        "typ": "JWT",
    }
    payload = {
        "username": user["username"],
        # "group": user.role,
        # "permission": user.id,
        "exp": int(time.time() + 3600),
    }
    token = jwt.encode(payload=payload, key=current_app.config.get('SECRET_KEY'), algorithm='HS256', headers=headers)
    return token


def validate_token(token, current_app):
    res = {
        "success": False
    }
    try:
        data = jwt.decode(jwt=token, key=current_app.config.get('SECRET_KEY'), algorithms=['HS256'])
        res["success"] = True
        res["data"] = data
    except ExpiredSignatureError:
        pass
    return res
