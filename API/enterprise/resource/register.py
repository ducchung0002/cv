from flask_restful import Resource
from flask import jsonify, request
from service.enterprise.enterprise_service import enterprise_service


class register(Resource):
    def post(self):
        name = request.json.get("name", None)
        email = request.json.get("email", None)
        role = request.json.get("role", None)
        password = request.json.get("password", None)
        
        try:
            app_ser = enterprise_service()
            app_ser.register(name, email,role,  password)
            return jsonify(msg="Create new account successed!", success=True)
        except Exception as exception:
            print(str(exception))
            return jsonify(msg=str(exception), success=False)