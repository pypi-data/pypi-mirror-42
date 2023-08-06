from flask import Blueprint

api_1_1_system = Blueprint('api_1_1', __name__)

from . import commonUserInfoViews
