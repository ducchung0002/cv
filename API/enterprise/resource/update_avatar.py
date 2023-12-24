from flask_restful import Resource
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from service.enterprise.enterprise_service import enterprise_service


class update_avatar(Resource):
    @jwt_required()
    def put(self):
        token = get_jwt_identity()  # dict {'id': 1, 'email': a@b.c}
        try:
            app_ser = enterprise_service()
            enterprise = app_ser.get_enterprise_by_id(token["id"])
            if enterprise and enterprise.email == token["email"]:
                avatar = request.files["avatar"].read()
                app_ser.update_avatar(enterprise.id, avatar)
                return jsonify(success=True, msg="Update avatar success!")
            else:
                return jsonify(success=False, msg="No enterprises is founded!")
        except Exception as exception:
            return jsonify(success=False, msg=str(exception))
