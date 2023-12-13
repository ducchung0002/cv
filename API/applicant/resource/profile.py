
from flask_restful import Resource
from flask import jsonify, request, send_file
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from service.applicant.applicant_service import applicant_service

import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # resource
AVATAR_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "images", "profile")

from werkzeug.utils import secure_filename

class profile(Resource):
    @jwt_required()
    def post(self):
        token = get_jwt_identity()  # dict {'id': 1, 'email': a@b.c}
        try:
            app_ser = applicant_service()
            applicant = app_ser.get_applicant_by_id(token["id"])
            if applicant and applicant.email == token["email"]:
                command = request.form.get("command")
                if command == "get_applicant":
                    return jsonify(applicant=applicant.jsonify(), success=True)
                if command == "get_avatar":
                    return send_file(request.form.get("image_path"))
            else:
                return jsonify(success=False, msg="No applicants is founded!")
        except Exception as exception:
            return jsonify(success=False, msg=str(exception))

    @jwt_required()
    def put(self):
        token = get_jwt_identity()  # dict {'id': 1, 'email': a@b.c}
        try:
            app_ser = applicant_service()
            applicant = app_ser.get_applicant_by_id(token["id"])
            if applicant and applicant.email == token["email"]:
                command = request.form.get("command")
                if command == "update_avatar":
                    avatar = request.files["avatar"]
                    if applicant.avatar_path:
                        avatar.save(applicant.avatar_path)
                    else:
                        avatar_path = os.path.join(AVATAR_DIR, str(applicant.id))
                        os.makedirs(avatar_path, exist_ok=True)
                        extension = os.path.splitext(secure_filename(avatar.filename))[1]
                        file_name = str(len([name for name in os.listdir(avatar_path)])) + extension
                        applicant.avatar_path = os.path.join(avatar_path, file_name)
                        avatar.save(applicant.avatar_path)
                        app_ser.update_avatar_path(applicant.id, applicant.avatar_path)
                    return send_file(applicant.avatar_path)
                if command == "update_profile":
                    app_ser.update_profile({"id": applicant.id} | request.form)
                    return jsonify(success=True, msg="Update profile information success!")
                return jsonify(success=False, msg="Update request not found!")
            else:
                return jsonify(success=False, msg="No applicants is founded!")
        except Exception as exception:
            return jsonify(success=False, msg=str(exception))