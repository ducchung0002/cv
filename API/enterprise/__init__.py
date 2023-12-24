from flask import Blueprint
from flask_restful import Api
from flask_cors import CORS

from API.enterprise.resource.login import login
from API.enterprise.resource.register import register
from API.enterprise.resource.profile import profile
enterprise_bp = Blueprint('enterprise', __name__)
CORS(enterprise_bp)
api = Api(enterprise_bp)
# api.add_resource()

api.add_resource(login, "/login")
api.add_resource(register, "/register")
api.add_resource(profile, "/profile")