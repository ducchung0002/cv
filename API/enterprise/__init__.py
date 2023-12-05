from flask import Blueprint
from flask_restful import Api
from flask_cors import CORS

enterprise_bp = Blueprint('enterprise', __name__)
CORS(enterprise_bp)
api = Api(enterprise_bp)
# api.add_resource()