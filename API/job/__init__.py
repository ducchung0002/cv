from flask import Blueprint
from flask_restful import Api
from flask_cors import CORS

job_bp = Blueprint('job', __name__)
CORS(job_bp)
api = Api(job_bp)
# api.add_resource()
