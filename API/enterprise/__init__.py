from flask import Blueprint
from flask_restful import Api
from flask_cors import CORS

from API.enterprise.resource.login import login
from API.enterprise.resource.register import register
from API.enterprise.resource.profile import profile
from API.enterprise.resource.admin import admin
from API.enterprise.resource.detail import detail
from API.enterprise.resource.recruitment import recruitment


enterprise_bp = Blueprint('enterprise', __name__)
CORS(enterprise_bp)
api = Api(enterprise_bp)
# api.add_resource()

api.add_resource(login, "/login")
api.add_resource(register, "/register")
api.add_resource(profile, "/profile")
api.add_resource(admin, "/admin")
api.add_resource(detail, "/detail")
api.add_resource(recruitment, "/recruitment")


