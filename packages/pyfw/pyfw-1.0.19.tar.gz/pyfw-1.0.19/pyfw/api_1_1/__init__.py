from flask import Blueprint

api_1_1 = Blueprint('api_1_1', __name__)

from . import commonUserInfoViews
