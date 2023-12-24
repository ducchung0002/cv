from flask_restful import Resource
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from service.applicant.applicant_service import applicant_service
from flask_jwt_extended import create_access_token

class application(Resource):
    @jwt_required()
    def get(self):
        token = get_jwt_identity()  # dict {'id': 1, 'email': a@b.c}
        try:
            app_ser = applicant_service()
            applicant = app_ser.get_all_application(applicant.id)
            if applicant and applicant.email == token["email"]:

                pass
            else:
                return jsonify(success=False, msg="Account does not exist!")
        except Exception as exception:
            return jsonify(success=False, msg=str(exception))