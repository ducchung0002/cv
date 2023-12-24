from flask import Flask
# blueprint
from API.database import database_bp
from API.applicant import applicant_bp
from API.enterprise import enterprise_bp
from API.job import job_bp
# CORS
from flask_cors import CORS
# JWT
from flask_jwt_extended import JWTManager

app = Flask(__name__, static_url_path="/static")

CORS(app)
JWTManager(app)

app.config["SECRET_KEY"] = "emyeucoquyen"
app.config["UPLOAD_FOLDER"] = "static/uploads/"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024


app.register_blueprint(database_bp, url_prefix="/database")
app.register_blueprint(applicant_bp, url_prefix="/applicant")
app.register_blueprint(enterprise_bp, url_prefix="/enterprise")
app.register_blueprint(job_bp, url_prefix="/job")


# @app.route('/get_image/<filename>')
# def get_image(filename):
#     return redirect(url_for("static", filename="uploads/" + filename), code=301)

# @app.route("/get_image/<filename>")
# def get_image(filename):
    # return send_file(app.config["UPLOAD_FOLDER"] + filename)