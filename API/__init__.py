from flask import Flask
from API.applicant import applicant_bp
from API.enterprise import enterprise_bp
from API.job import job_bp
from flask_cors import CORS
from flask_jwt_extended import JWTManager
app = Flask(__name__)
CORS(app)
JWTManager(app)
app.config["SECRET_KEY"] = "emyeucoquyen"

app.register_blueprint(applicant_bp, url_prefix="/applicant")
app.register_blueprint(enterprise_bp, url_prefix="/enterprise")
app.register_blueprint(job_bp, url_prefix="/job")


