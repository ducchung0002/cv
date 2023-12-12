class skill_type:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def jsonify(self):
        return {
            "id": self.id,
            "name": self.name
        }