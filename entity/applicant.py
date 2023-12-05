import base64

class applicant:
    def __init__(self, app_json: dict):
        # print("json:", app_json)
        self.id = app_json.get("id", None)
        self.avatar = app_json.get("avatar", None)
        self.name = app_json.get("name", None)
        self.birthdate = app_json.get("birthdate", None)
        self.gender = app_json.get("gender", None)
        self.phone = app_json.get("phone", None)
        self.address = app_json.get("address", None)
        self.email = app_json.get("email", None)
        self.password_hashed = app_json.get("password_hashed", None)
        self.facebook = app_json.get("facebook", None)
        self.github = app_json.get("github", None)
        self.self_introduction = app_json.get("self_introduction", None)
        self.education_school_name = app_json.get("education_school_name", None)
        self.education_major = app_json.get("education_major", None)
        self.education_school_start_date = app_json.get("education_school_start_date", None)
        self.education_school_end_date = app_json.get("education_school_end_date", None)
        self.internship_enterprise_name = app_json.get("internship_enterprise_name", None)
        self.internship_position = app_json.get("internship_position", None)
        self.internship_start_date = app_json.get("internship_start_date", None)
        self.internship_end_date = app_json.get("internship_end_date", None)

    def jsonify(self):
        return {
            "id": self.id,
            "avatar": base64.b64encode(self.avatar).decode("utf-8") if self.avatar else self.avatar,
            "name": self.name,
            "birthdate": self.birthdate,
            "gender": self.gender,
            "phone": self.phone,
            "address": self.address,
            "email": self.email,
            "password_hashed": self.password_hashed,
            "facebook": self.facebook,
            "github": self.github,
            "self_introduction": self.self_introduction,
            "education_school_name": self.education_school_name,
            "education_major": self.education_major,
            "education_school_start_date": self.education_school_start_date,
            "education_school_end_date": self.education_school_end_date,
            "internship_enterprise_name": self.internship_enterprise_name,
            "internship_position": self.internship_position,
            "internship_start_date": self.internship_start_date,
            "internship_end_date": self.internship_end_date
        }

    def identity(self):
        return {
            "id": self.id,
            "email": self.email
        }