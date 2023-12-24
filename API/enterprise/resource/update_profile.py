from flask_restful import Resource
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from service.enterprise.enterprise_service import enterprise_service


class update_profile(Resource):
    @jwt_required()
    def put(self):
        token = get_jwt_identity()  # dict {'id': 1, 'email': a@b.c}
        try:
            app_ser = enterprise_service()
            enterprise = app_ser.get_enterprise_by_id(token["id"])
            if enterprise and enterprise.email == token["email"]:
                app_ser.update_profile({"id": enterprise.id} | request.json)
                return jsonify(success=True, msg="Update profile information success!")
            else:
                return jsonify(success=False, msg="No enterprises is founded!")
        except:
            return jsonify(success=False, msg="Access token is not valid!")
