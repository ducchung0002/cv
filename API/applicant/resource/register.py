from flask_restful import Resource
from flask import jsonify, request
from service.applicant.applicant_service import applicant_service


class register(Resource):
    def post(self):
        name = request.json.get("name", None)
        birthdate = request.json.get("birthdate", None)
        gender = request.json.get("gender", 1)
        email = request.json.get("email", None)
        password = request.json.get("password", None)
        try:
            app_ser = applicant_service()
            app_ser.register(name, birthdate, gender, email, password)
            return jsonify(msg="Create new account successed!", success=True)
        except Exception as exception:
            return jsonify(msg=str(exception), success=False)