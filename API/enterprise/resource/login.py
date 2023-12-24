from flask_restful import Resource
from flask import jsonify, request
from service.enterprise.enterprise_service import enterprise_service

from flask_jwt_extended import create_access_token

class login(Resource):
    def post(self):
        email = request.json.get("email", None)
        password = request.json.get("password", None)
        app_ser = enterprise_service()
        enterprise = app_ser.valid_login(email, password)
        if enterprise:
            return jsonify(success=True, access_token=create_access_token(identity=enterprise.identity()), msg="Login success!")
        else:
            return jsonify(success=False, msg="Account does not exist!")