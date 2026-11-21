"""IPAtlas Flask application factory."""
import logging
import os

from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException

from . import storage
from .config import Config
from .errors import IPAtlasError
from .routes import bp

logger = logging.getLogger(__name__)


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)
    app.json.sort_keys = False

    db_path = app.config["DB_PATH"]
    if not os.path.isabs(db_path):
        db_path = os.path.join(os.path.dirname(app.root_path), db_path)
    app.config["DB_PATH"] = db_path
    storage.init_db(db_path)

    app.register_blueprint(bp)
    _register_error_handlers(app)
    return app


def _error_body(code: str, message: str) -> dict:
    return {"error": {"code": code, "message": message}}


def _register_error_handlers(app: Flask) -> None:
    @app.errorhandler(IPAtlasError)
    def handle_app_error(exc: IPAtlasError):
        return jsonify(_error_body(exc.code, exc.message)), exc.status_code

    @app.errorhandler(HTTPException)
    def handle_http_error(exc: HTTPException):
        if request.path.startswith("/api/"):
            code = (exc.name or "error").lower().replace(" ", "_")
            return jsonify(_error_body(code, exc.description or exc.name)), exc.code
        return exc

    @app.errorhandler(Exception)
    def handle_unexpected(exc: Exception):
        logger.exception("Unhandled error")
        if request.path.startswith("/api/"):
            return jsonify(_error_body("internal_error", "Unexpected server error.")), 500
        raise exc
