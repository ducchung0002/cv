from flask_restful import Resource
from flask import jsonify

from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required


from service.enterprise.enterprise_service import enterprise_service


class profile(Resource):
    @jwt_required()
    def get(self):
        token = get_jwt_identity()  # dict {'id': 1, 'email': a@b.c}
        try:
            app_ser = enterprise_service()
            print(token)
            enterprise = app_ser.get_enterprise_by_id(token["enterprise_id"])
            print(enterprise.email)
            if enterprise and enterprise.email == token["email"]:
                return jsonify(enterprise=enterprise.jsonify(), success=True)
            else:
                return jsonify(success=False, msg="No enterprises is founded!")
        except Exception as exception:
            print(exception)
            return jsonify(success=False, msg=str(exception))
