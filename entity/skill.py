class skill:
    def __init__(self, id, skill_type_id, name):
        self.id = id
        self.skill_type_id = skill_type_id
        self.name = name

    def jsonify(self):
        return {
            "id": self.id,
            "skill_type_id": self.skill_type_id,
            "name": self.name
        }