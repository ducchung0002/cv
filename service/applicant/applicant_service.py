import io

import pyodbc
import base64
from werkzeug.security import generate_password_hash, check_password_hash
from service import CONNECTION_STRING
from entity.applicant import applicant


class applicant_service:
    def register(self, name, birthdate, gender, email, password):
        hashed_pass = generate_password_hash(password)
        try:
            connection = pyodbc.connect(CONNECTION_STRING)
            cursor = connection.cursor()
            cursor.execute("INSERT INTO applicant(name, birthdate, gender, email, password_hashed) VALUES (?,?,?,?,?)",
                           (name, birthdate, gender, email, hashed_pass))
            cursor.commit()
            cursor.close()
            connection.close()
        except:
            raise

    def valid_login(self, email, password):
        try:
            applicant = self.get_applicant_by_email(email)
            if applicant and check_password_hash(applicant.password_hashed, password):
                return applicant
            return None
        except:
            raise

    def get_applicant_by_id(self, id):
        try:
            connection = pyodbc.connect(CONNECTION_STRING)
            cursor = connection.cursor()
            cursor.execute(
                "SELECT id,avatar,name,birthdate,gender,phone,address,email,password_hashed,facebook,github,self_introduction,education_school_name,education_major,education_school_start_date,education_school_end_date,internship_enterprise_name,internship_position,internship_start_date,internship_end_date  FROM applicant WHERE id = ?",
                (id,))
            record = cursor.fetchone()
            cursor.close()
            connection.close()

            if record:
                return applicant(app_json={"id": record[0], "avatar": record[1], "name": record[2], "birthdate": record[3], "gender": record[4], "phone": record[5], "address": record[6], "email": record[7], "password_hashed": record[8], "facebook": record[9], "github": record[10], "self_introduction": record[11], "education_school_name": record[12], "education_major": record[13], "education_school_start_date": record[14], "education_school_end_date": record[15], "internship_enterprise_name": record[16], "internship_position": record[17], "internship_start_date": record[18], "internship_end_date": record[19]})
            return None

        except:
            raise

    def get_applicant_by_email(self, email):
        try:
            connection = pyodbc.connect(CONNECTION_STRING)
            cursor = connection.cursor()
            cursor.execute(
                "SELECT id,avatar,name,birthdate,gender,phone,address,email,password_hashed,facebook,github,self_introduction,education_school_name,education_major,education_school_start_date,education_school_end_date,internship_enterprise_name,internship_position,internship_start_date,internship_end_date  FROM applicant WHERE email = ?",
                (email,))
            record = cursor.fetchone()
            cursor.close()
            connection.close()
            if record:
                return applicant(app_json={"id": record[0], "avatar": record[1], "name": record[2], "birthdate": record[3], "gender": record[4], "phone": record[5], "address": record[6], "email": record[7], "password_hashed": record[8], "facebook": record[9], "github": record[10], "self_introduction": record[11], "education_school_name": record[12], "education_major": record[13], "education_school_start_date": record[14], "education_school_end_date": record[15], "internship_enterprise_name": record[16], "internship_position": record[17], "internship_start_date": record[18], "internship_end_date": record[19]})
            return None

        except:
            raise

    def update_profile(self, app_json):
        try:
            name, birthdate, gender, phone, address, facebook, github, self_introduction, education_school_name, education_major, education_school_start_date, education_school_end_date, internship_enterprise_name, internship_position, internship_start_date, internship_end_date, id = app_json["name"], app_json["birthdate"], app_json["gender"], app_json["phone"], app_json["address"], app_json["facebook"], app_json["github"], app_json["self_introduction"], app_json["education_school_name"], app_json["education_major"], app_json["education_school_start_date"], app_json["education_school_end_date"], app_json["internship_enterprise_name"], app_json["internship_position"], app_json["internship_start_date"], app_json["internship_end_date"], app_json["id"]

            birthdate = None if not birthdate else birthdate
            education_school_start_date = None if not education_school_start_date else education_school_start_date
            education_school_end_date = None if not education_school_end_date else education_school_end_date
            internship_start_date = None if not internship_start_date else internship_start_date
            internship_end_date = None if not internship_end_date else internship_end_date

            connection = pyodbc.connect(CONNECTION_STRING)
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE applicant SET name=?,birthdate=?,gender=?,phone=?,address=?,facebook=?,github=?,self_introduction=?,education_school_name=?,education_major=?,education_school_start_date=?,education_school_end_date=?,internship_enterprise_name=?,internship_position=?,internship_start_date=?,internship_end_date=? WHERE id=?",
                                 (name, birthdate, gender, phone, address, facebook, github, self_introduction, education_school_name, education_major, education_school_start_date, education_school_end_date, internship_enterprise_name, internship_position, internship_start_date, internship_end_date, id))
            cursor.commit()
            cursor.close()
            connection.close()
        except:
            raise

    def update_avatar(self, id, avatar):
        try:
            connection = pyodbc.connect(CONNECTION_STRING)
            cursor = connection.cursor()
            cursor.execute("UPDATE applicant SET avatar=? WHERE id=?", (avatar, id))
            cursor.commit()
            cursor.close()
            connection.close()
        except:
            raise
