from flask import Blueprint
from flask_restful import Api
from flask_cors import CORS
# Resource
from API.database.resource.experience import experience
from API.database.resource.skill import skill
from API.database.resource.skill_type import skill_type

database_bp = Blueprint("database", __name__)
CORS(database_bp)
api = Api(database_bp)


api.add_resource(experience, "/experience")
api.add_resource(skill, "/skill")
api.add_resource(skill_type, "/skill_type")