from flask import Blueprint

bp = Blueprint('data_management', __name__)

from app.data_management import routes