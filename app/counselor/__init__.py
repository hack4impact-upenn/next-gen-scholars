from flask import Blueprint

counselor = Blueprint('counselor', __name__)

from . import views  # noqa
