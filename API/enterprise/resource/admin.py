from flask_restful import Resource
from flask import jsonify, request, send_file
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from service.enterprise.enterprise_service import enterprise_service
import json

import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # resource
AVATAR_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "images", "profile")

from werkzeug.utils import secure_filename


class admin(Resource):
    @jwt_required()
    def get(self):
        token = get_jwt_identity()  # dict {'id': 1, 'email': a@b.c}
        try:
            app_ser = enterprise_service()
            enterprises = app_ser.get_all_enterprises()
          #   print(enterprises)
            enterprises_json = json.dumps(enterprises)
            return jsonify(enterprises=enterprises_json, success=True)
        except Exception as exception:
            print(exception)
            return jsonify(success=False, msg=str(exception))
