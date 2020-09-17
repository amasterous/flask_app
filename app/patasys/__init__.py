from flask import Blueprint

bp = Blueprint('patasys', __name__)

from app.patasys import routes