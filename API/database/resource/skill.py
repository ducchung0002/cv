from flask_restful import Resource
from flask import jsonify
from service.db_service import db_service
class skill(Resource):
    def get(self):
        try:
            return jsonify(success=True, skill=(db_service()).get_all_skill())
        except Exception as exception:
            return jsonify(success=False, msg=str(exception))