from flask_restful import Resource
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from service.applicant.applicant_service import applicant_service


class update_avatar(Resource):
    @jwt_required()
    def put(self):
        token = get_jwt_identity()  # dict {'id': 1, 'email': a@b.c}
        try:
            app_ser = applicant_service()
            applicant = app_ser.get_applicant_by_id(token["id"])
            if applicant and applicant.email == token["email"]:
                avatar = request.files["avatar"].read()
                app_ser.update_avatar(applicant.id, avatar)
                return jsonify(success=True, msg="Update avatar success!")
            else:
                return jsonify(success=False, msg="No applicants is founded!")
        except Exception as exception:
            return jsonify(success=False, msg=str(exception))
