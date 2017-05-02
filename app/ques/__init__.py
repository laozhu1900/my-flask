from flask import Blueprint

ques = Blueprint('ques', __name__)

from . import views

