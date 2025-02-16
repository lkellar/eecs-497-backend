from flask import jsonify

def build_error(message: str, status_code: int):
    response = jsonify({
        "error": message
    })
    response.status_code = status_code
    return response

from backend.routes.auth import register_account, login_account, logout_account
from backend.routes.lang import list_languages