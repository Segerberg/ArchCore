from flask import Blueprint

bp = Blueprint('preservation_planning', __name__)

from app.preservation_planning import routes