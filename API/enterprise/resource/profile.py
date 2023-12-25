from flask_restful import Resource
from flask import jsonify, request, send_file
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from service.enterprise.enterprise_service import enterprise_service

import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # resource
AVATAR_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "images", "profile")

from werkzeug.utils import secure_filename


class profile(Resource):
    @jwt_required()
    def get(self):
        token = get_jwt_identity()  # dict {'id': 1, 'email': a@b.c}
        try:
            app_ser = enterprise_service()
            print(token)
            enterprise = app_ser.get_enterprise_by_id(token["enterprise_id"])
            print(enterprise.email)
            if enterprise and enterprise.email == token["email"]:
                return jsonify(enterprise=enterprise.jsonify(), success=True)
            else:
                return jsonify(success=False, msg="No enterprises is founded!")
        except Exception as exception:
            print(exception)
            return jsonify(success=False, msg=str(exception))
    @jwt_required()
    def put(self):
        token = get_jwt_identity()  # dict {'id': 1, 'email': a@b.c}
        try:
            app_ser = enterprise_service()
            enterprise = app_ser.get_enterprise_by_id(token["enterprise_id"])
            if enterprise and enterprise.email == token["email"]:
                command = request.form.get("command")
                if command == "update_avatar":
                    avatar = request.files["avatar"]
                    if enterprise.avatar_path:
                        avatar.save(enterprise.avatar_path)
                    else:
                        avatar_path = os.path.join(AVATAR_DIR, str(enterprise.id))
                        os.makedirs(avatar_path, exist_ok=True)
                        extension = os.path.splitext(secure_filename(avatar.filename))[1]
                        file_name = str(len([name for name in os.listdir(avatar_path)])) + extension
                        enterprise.avatar_path = os.path.join(avatar_path, file_name)
                        avatar.save(enterprise.avatar_path)
                        app_ser.update_avatar_path(enterprise.id, enterprise.avatar_path)
                    return send_file(enterprise.avatar_path)
                if command == "update_profile":
                    print("enterprise.enterprise_id", enterprise.enterprise_id)
                    app_ser.update_profile({"enterprise_id": enterprise.enterprise_id} | request.form)
                    return jsonify(success=True, msg="Update profile information success!")
                return jsonify(success=False, msg="Update request not found!")
            else:
                return jsonify(success=False, msg="No enterprises is founded!")
        except Exception as exception:
            return jsonify(success=False, msg=str(exception))
