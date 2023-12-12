from flask_restful import Resource
from flask import jsonify
from service.db_service import db_service
class skill_type(Resource):
    def get(self):
        try:
            return jsonify(success=True, skill_type=(db_service()).get_all_skill_type())
        except Exception as exception:
            return jsonify(success=False, msg=str(exception))