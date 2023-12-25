import base64

class enterprise:
    def __init__(self, app_json: dict):
        self.name = app_json.get("name", None)
        self.email = app_json.get("email", None)
        self.password_hashed = app_json.get("password_hashed", None)
        self.role = app_json.get("role", None)
        self.enterprise_id = app_json.get("enterprise_id", None)
        self.homepage = app_json.get("homepage", None)
        self.avatar = app_json.get("avatar", None)
    def jsonify(self):
        return {
            "name": self.name,
            "email": self.email,
            "password_hashed": self.password_hashed,
            "role": self.role,
            "enterprise_id": self.enterprise_id,
            "homepage": self.homepage,
            "avatar": self.avatar
        }

    def identity(self):
        return {
            "email": self.email,
            "enterprise_id": self.enterprise_id,
            "role": self.role
        }
