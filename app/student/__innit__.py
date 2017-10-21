from flask import Blueprint
	# this student folder is not currently being used
	# use case: dislaying student profile information
student = Blueprint('student', __name__)

from . import views  # noqa