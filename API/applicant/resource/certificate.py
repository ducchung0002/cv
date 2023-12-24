from flask import jsonify, request, send_file
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from service.applicant.applicant_service import applicant_service
import os
import shutil
from werkzeug.utils import secure_filename

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # resource
CERTIFICATE_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "images", "certificate")


class certificate(Resource):
    @jwt_required()
    def get(self):
        token = get_jwt_identity()  # dict {'id': 1, 'email': a@b.c}
        try:
            app_ser = applicant_service()
            applicant = app_ser.get_applicant_by_id(token["id"])
            if applicant and applicant.email == token["email"]:
                command = request.args.get("command")
                if command == "get_certificate_image":
                    return send_file(request.args.get("image_path"))
                if command == "get_certificate":
                    return jsonify(success=True, applicant_certificate=app_ser.get_applicant_certificate(applicant.id))
            else:
                return jsonify(success=False, msg="No applicants is founded!")
        except Exception as exception:
            return jsonify(success=False, msg=str(exception))

    @jwt_required()
    def post(self):
        token = get_jwt_identity()  # dict {'id': 1, 'email': a@b.c}
        try:
            app_ser = applicant_service()
            applicant = app_ser.get_applicant_by_id(token["id"])
            if applicant and applicant.email == token["email"]:
                command = request.form.get("command")
                if command == "insert_certificate_image":
                    # get applicant certificate id
                    applicant_certificate_id = request.form.get("applicant_certificate_id")
                    # create dir to save image
                    certificate_image_dir_path = os.path.join(CERTIFICATE_DIR, str(applicant.id), applicant_certificate_id)
                    os.makedirs(certificate_image_dir_path, exist_ok=True)
                    # Get the image extension
                    image = request.files["image"]
                    extension = os.path.splitext(secure_filename(image.filename))[1]
                    # update path in database and get file name
                    applicant_certificate_image_id, image_path = app_ser.insert_applicant_certificate_image(applicant_certificate_id, certificate_image_dir_path, extension)
                    # save image
                    image.save(image_path)
                    return jsonify(success=True, applicant_certificate_image_id=applicant_certificate_image_id, image_path=image_path)
                elif command == "insert_certificate":
                    applicant_certificate_id = app_ser.insert_applicant_certificate(applicant.id)
                    return jsonify(success=True, applicant_certificate_id=applicant_certificate_id)
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
                if command == "update_applicant_certificate":
                    applicant_certificate_id = request.form.get("applicant_certificate_id")
                    certificate_name = request.form.get("certificate_name")
                    received_date = request.form.get("received_date")
                    app_ser.update_applicant_certificate(applicant_certificate_id, certificate_name, received_date)
                    return jsonify(success=True, msg="Update applicant skill successfully!")
                return jsonify(success=False, msg="Request not Found!")
            else:
                return jsonify(success=False, msg="No applicants is founded!")
        except Exception as exception:
            return jsonify(success=False, msg=str(exception))

    @jwt_required()
    def delete(self):
        token = get_jwt_identity()  # dict {'id': 1, 'email': a@b.c}
        try:
            app_ser = applicant_service()
            applicant = app_ser.get_applicant_by_id(token["id"])
            if applicant and applicant.email == token["email"]:
                command = request.form.get("command")
                print("command: ", command)
                if command == "delete_applicant_certificate":
                    applicant_certificate_id = request.form.get("applicant_certificate_id")
                    applicant_certificate_image_dir = os.path.join(CERTIFICATE_DIR, str(applicant.id), str(applicant_certificate_id))
                    print("applicant certificate image dir", applicant_certificate_image_dir)
                    if os.path.exists(applicant_certificate_image_dir):
                        shutil.rmtree(applicant_certificate_image_dir)
                    app_ser.delete_applicant_certificate(applicant_certificate_id)
                    return jsonify(success=True, msg="Delete applicant certificate successfully!")
                if command == "delete_applicant_certificate_image":
                    image_path = app_ser.delete_applicant_certificate_image(request.form.get("applicant_certificate_image_id"))
                    if os.path.isfile(image_path):
                        os.remove(image_path)
                    return jsonify(success=True, msg="Delete applicant certificate image successfully!")
                return jsonify(success=False, msg="No command is found!")
            else:
                return jsonify(success=False, msg="No applicants is founded!")
        except Exception as exception:
            return jsonify(success=False, msg=str(exception))
