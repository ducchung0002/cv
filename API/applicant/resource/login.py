from flask_restful import Resource
from flask import jsonify, request
from service.applicant.applicant_service import applicant_service

from flask_jwt_extended import create_access_token

class login(Resource):
    def post(self):
        try:
            email = request.json.get("email", None)
            password = request.json.get("password", None)
            app_ser = applicant_service()
            applicant = app_ser.valid_login(email, password)
            if applicant:
                return jsonify(success=True, access_token=create_access_token(identity=applicant.identity()), msg="Login success!")
            else:
                return jsonify(success=False, msg="Account does not exist!")
        except Exception as exception:
            return jsonify(success=False, msg=str(exception))