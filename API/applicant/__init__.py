from flask import Blueprint
from flask_restful import Api
from flask_cors import CORS

# Resource
from API.applicant.resource.register import register
from API.applicant.resource.login import login
from API.applicant.resource.profile import profile
from API.applicant.resource.skill import skill
from API.applicant.resource.certificate import certificate

applicant_bp = Blueprint("applicant", __name__)

CORS(applicant_bp)
api = Api(applicant_bp)

api.add_resource(register, "/register")
api.add_resource(login, "/login")
api.add_resource(profile, "/profile")
api.add_resource(skill, "/skill")
api.add_resource(certificate, "/certificate")
