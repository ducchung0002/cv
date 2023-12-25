
from flask_restful import Resource
from flask import jsonify, request, send_file
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from service.enterprise.enterprise_service import enterprise_service

import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # resource
AVATAR_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "images", "profile")

from werkzeug.utils import secure_filename

class recruitment(Resource):

    @jwt_required()
    def post(self):
        token = get_jwt_identity()  # dict {'id': 1, 'email': a@b.c}
        try:
            app_ser = enterprise_service()
            enterprise = app_ser.get_enterprise_by_id(token["enterprise_id"])
            if enterprise and enterprise.email == token["email"]:
                command = request.form.get("command")
                if command == "add_recruitment":
                    app_ser.add_recruitment({"enterprise_id": enterprise.enterprise_id} | request.form)
                    return jsonify(success=True, msg="Add recruitment information success!")
                return jsonify(success=False, msg="Update request not found!")
            else:
                return jsonify(success=False, msg="No enterprises is founded!")
        except Exception as exception:
            return jsonify(success=False, msg=str(exception))