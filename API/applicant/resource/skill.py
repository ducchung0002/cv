from flask_restful import Resource
from flask import jsonify, request

from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

from service.applicant.applicant_service import applicant_service


class skill(Resource):
    @jwt_required()
    def get(self):
        token = get_jwt_identity()  # dict {'id': 1, 'email': a@b.c}
        try:
            app_ser = applicant_service()
            applicant = app_ser.get_applicant_by_id(token["id"])
            if applicant and applicant.email == token["email"]:
                return jsonify(success=True, applicant_skill=app_ser.get_applicant_skill(applicant.id))
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
                skill_id = request.json.get("skill_id")
                experience_id = request.json.get("experience_id")
                applicant_skill_id = app_ser.insert_applicant_skill(applicant.id, skill_id, experience_id)
                return jsonify(success=True, msg="Insert applicant skill successfully!", applicant_skill_id=applicant_skill_id)
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
                id = request.json.get("id")
                skill_id = request.json.get("skill_id")
                experience_id = request.json.get("experience_id")
                app_ser.update_applicant_skill(id, skill_id, experience_id)
                return jsonify(success=True, msg="Update applicant skill successfully!")
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
                id = request.json.get("id")
                app_ser.delete_applicant_skill(id)
                return jsonify(success=True, msg="Delete applicant skill successfully!")
            else:
                return jsonify(success=False, msg="No applicants is founded!")
        except Exception as exception:
            return jsonify(success=False, msg=str(exception))
