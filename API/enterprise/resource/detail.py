from flask_restful import Resource
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from service.enterprise.enterprise_service import enterprise_service
import os
import requests
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # Thư mục resource
AVATAR_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "images", "profile")

class detail(Resource):
    @jwt_required()
    def get(self):
        try:
            print("------------------------------------------")
            token = get_jwt_identity()  # Trích xuất thông tin từ token (VD: {'id': 1, 'email': 'a@b.c', 'enterprise_id': 123})
            app_ser = enterprise_service()
            enterprise_id = request.args.get('id')
            print(enterprise_id)
            # Lấy thông tin doanh nghiệp dựa trên enterprise_id từ token
            enterprise = app_ser.get_enterprise_by_id(enterprise_id)
            
            # Kiểm tra nếu doanh nghiệp tồn tại và email trùng khớp với email từ token
            if enterprise :
                return jsonify(enterprise=enterprise.jsonify(), success=True)
            else:
                return jsonify(success=False, msg="No enterprise found for the provided credentials.")
        except Exception as exception:
            return jsonify(success=False, msg=str(exception))
