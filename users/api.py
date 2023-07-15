from flask import Blueprint, render_template, abort

users_bp = Blueprint('users_bp', __name__, url_prefix="/users")

@users_bp.route('/')
def get():
    return "GET /users "