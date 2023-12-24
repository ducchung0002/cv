import traceback

from flask import jsonify, request
from flask_restful import Resource
from service.applicant.applicant_service import applicant_service


class reset_password(Resource):
    def get(self):
        try:
            email = request.args.get("email", None)
            app_ser = applicant_service()
            applicant = app_ser.get_applicant_by_email(email)
            if applicant:
                return jsonify(success=app_ser.send_verify_code(email))
            else:
                return jsonify(success=False, msg="Account does not exist!")
        except Exception as exception:
            print("Request recovery code exception: ", exception)
            traceback.print_exc()
            return jsonify(success=False, msg=str(exception))

    def post(self):
        try:
            email = request.form.get("email", None)
            recovery_code = request.form.get("recovery_code", None)
            app_ser = applicant_service()
            return jsonify(success=app_ser.reset_password(email, recovery_code))
        except Exception as exception:
            traceback.print_exc()
            return jsonify(success=False, msg=str(exception))
