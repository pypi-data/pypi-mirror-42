from flask import Blueprint, render_template, jsonify
from flask_security import login_required
from jinja2 import TemplateNotFound

from meltano.api.security import api_auth_required


root = Blueprint("root", __name__)


@root.errorhandler(500)
def internal_error(exception):
    logger.info(f"[{request.remote_addr}] request: {now}, error: {exception}")
    return jsonify({"error": str(exception)}), 500


@root.route("/model")
@root.route("/")
@login_required
def analyze():
    try:
        return render_template("analyze.html")
    except TemplateNotFound:
        return "Please run `yarn build` from src/analyze."


@root.route("/drop")
@api_auth_required
def drop_it():
    from .sqlhelper import SqlHelper

    SqlHelper().reset_db()
    return jsonify({"dropped_it": "like it's hot"})
