from flask import jsonify, Response, current_app
from werkzeug.exceptions import HTTPException


class JsonResponse(Response):
    """Render Json if object is dict, list, MongoEngine object"""

    @classmethod
    def force_type(cls, res, environ=None):
        if isinstance(res, (dict, list)):
            resp = jsonify(res)
            resp.code = 200
        return super(JsonResponse, cls).force_type(res, environ)


def errors_handler(e):
    code = 500
    error = str(e)

    if isinstance(e, HTTPException):
        code = e.code
        error = e.description

    for _e_cls, _code in current_app.config.get('ERROR_MAPPINGS', []):
        if isinstance(e, _e_cls):
            code = _code

    return jsonify(error=error), code
