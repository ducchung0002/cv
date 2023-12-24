import pyodbc
import os

from werkzeug.security import generate_password_hash, check_password_hash
from entity.applicant import applicant
from service import CONNECTION_STRING


class applicant_service:
    def register(self, name, birthdate, gender, email, password):
        hashed_pass = generate_password_hash(password)
        try:
            connection = pyodbc.connect(CONNECTION_STRING)
            cursor = connection.cursor()
            cursor.execute("INSERT INTO applicant(name, birthdate, gender, email, password_hashed) VALUES (?,?,?,?,?)", (name, birthdate, gender, email, hashed_pass))
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
            cursor.execute("SELECT id,avatar_path,name,birthdate,gender,phone,address,email,password_hashed,facebook,github,self_introduction,education_school_name,education_major,education_school_start_date,education_school_end_date,internship_enterprise_name,internship_position,internship_start_date,internship_end_date  FROM applicant WHERE id = ?", (id,))
            record = cursor.fetchone()
            cursor.close()
            connection.close()

            if record:
                return applicant(app_json={"id": record[0], "avatar_path": record[1], "name": record[2], "birthdate": record[3], "gender": record[4], "phone": record[5], "address": record[6], "email": record[7], "password_hashed": record[8], "facebook": record[9], "github": record[10], "self_introduction": record[11], "education_school_name": record[12], "education_major": record[13], "education_school_start_date": record[14], "education_school_end_date": record[15], "internship_enterprise_name": record[16], "internship_position": record[17], "internship_start_date": record[18], "internship_end_date": record[19]})
            return None
        except:
            raise

    def get_applicant_by_email(self, email):
        try:
            connection = pyodbc.connect(CONNECTION_STRING)
            cursor = connection.cursor()
            cursor.execute("SELECT id,avatar_path,name,birthdate,gender,phone,address,email,password_hashed,facebook,github,self_introduction,education_school_name,education_major,education_school_start_date,education_school_end_date,internship_enterprise_name,internship_position,internship_start_date,internship_end_date  FROM applicant WHERE email = ?", (email,))
            record = cursor.fetchone()
            cursor.close()
            connection.close()
            if record:
                return applicant(app_json={"id": record[0], "avatar_path": record[1], "name": record[2], "birthdate": record[3], "gender": record[4], "phone": record[5], "address": record[6], "email": record[7], "password_hashed": record[8], "facebook": record[9], "github": record[10], "self_introduction": record[11], "education_school_name": record[12], "education_major": record[13], "education_school_start_date": record[14], "education_school_end_date": record[15], "internship_enterprise_name": record[16], "internship_position": record[17], "internship_start_date": record[18], "internship_end_date": record[19]})
            return None
        except:
            raise

    def update_profile(self, app_json):
        try:
            (name, birthdate, gender, phone, address, facebook, github,
             self_introduction, education_school_name, education_major,
             education_school_start_date, education_school_end_date,
             internship_enterprise_name, internship_position,
             internship_start_date, internship_end_date, id) = (
                app_json["name"], app_json["birthdate"], app_json["gender"], app_json["phone"],
                app_json["address"], app_json["facebook"], app_json["github"], app_json["self_introduction"],
                app_json["education_school_name"], app_json["education_major"],
                app_json["education_school_start_date"], app_json["education_school_end_date"],
                app_json["internship_enterprise_name"], app_json["internship_position"],
                app_json["internship_start_date"], app_json["internship_end_date"], app_json["id"])

            birthdate = None if not birthdate else birthdate
            education_school_start_date = None if not education_school_start_date else education_school_start_date
            education_school_end_date = None if not education_school_end_date else education_school_end_date
            internship_start_date = None if not internship_start_date else internship_start_date
            internship_end_date = None if not internship_end_date else internship_end_date

            connection = pyodbc.connect(CONNECTION_STRING)
            cursor = connection.cursor()
            sql = """
                UPDATE applicant 
                SET name=?,birthdate=?,gender=?,phone=?,address=?,facebook=?,github=?,
                self_introduction=?,education_school_name=?,education_major=?,education_school_start_date=?,
                education_school_end_date=?,internship_enterprise_name=?,internship_position=?,
                internship_start_date=?,internship_end_date=? 
                WHERE id=?
            """
            placeholder = (name, birthdate, gender, phone, address, facebook, github, self_introduction, education_school_name,
                           education_major, education_school_start_date, education_school_end_date, internship_enterprise_name,
                           internship_position, internship_start_date, internship_end_date, id)
            cursor.execute(sql, placeholder)
            cursor.commit()
            cursor.close()
            connection.close()
        except:
            raise

    def update_avatar_path(self, id, avatar_path):
        try:
            connection = pyodbc.connect(CONNECTION_STRING)
            cursor = connection.cursor()
            cursor.execute("UPDATE applicant SET avatar_path=? WHERE id=?", (avatar_path, id))
            cursor.commit()
            cursor.close()
            connection.close()
        except:
            raise
    # applicant skill
    def get_applicant_skill(self, id):
        try:
            connection = pyodbc.connect(CONNECTION_STRING)
            cursor = connection.cursor()
            sql = """
                SELECT applicant_skill.id, skill_id, skill_type_id, experience_id
                FROM applicant_skill 
                    JOIN skill ON applicant_skill.skill_id = skill.id 
                WHERE applicant_id=?
            """
            cursor.execute(sql, (id,))
            records = cursor.fetchall()
            cursor.close()
            connection.close()
            applicant_skills = []
            for record in records:
                applicant_skills.append({
                    "id": record[0],
                    "skill_id": record[1],
                    "skill_type_id": record[2],
                    "experience_id": record[3],
                })
            return applicant_skills
        except:
            raise

    def delete_applicant_skill(self, id):
        try:
            connection = pyodbc.connect(CONNECTION_STRING)
            cursor = connection.cursor()
            cursor.execute("DELETE FROM applicant_skill WHERE id=?", (id,))
            cursor.commit()
            cursor.close()
            connection.close()
        except:
            raise

    def update_applicant_skill(self, id, skill_id, experience_id):
        try:
            connection = pyodbc.connect(CONNECTION_STRING)
            cursor = connection.cursor()
            cursor.execute("UPDATE applicant_skill SET skill_id=?, experience_id=? WHERE id=?", (skill_id, experience_id, id))
            cursor.commit()
            cursor.close()
            connection.close()
        except:
            raise

    def insert_applicant_skill(self, id, skill_id, experience_id):
        try:
            connection = pyodbc.connect(CONNECTION_STRING)
            cursor = connection.cursor()
            cursor.execute("INSERT INTO applicant_skill(applicant_id, skill_id, experience_id) VALUES(?, ?, ?)", (id, skill_id, experience_id))
            cursor.commit()

            cursor.execute("SELECT MAX(id) FROM applicant_skill")
            record_id = cursor.fetchone()[0]

            cursor.close()
            connection.close()

            return record_id
        except:
            raise
    # applicant certificate
    def get_applicant_certificate(self, applicant_id):
        try:
            connection = pyodbc.connect(CONNECTION_STRING)
            cursor = connection.cursor()
            cursor.execute("SELECT id, name, received_date FROM applicant_certificate WHERE applicant_id=?", (applicant_id,))
            records = cursor.fetchall()
            all_certificate = []
            for record in records:
                cer = {
                    "id": record[0], "name": record[1],
                    "received_date": record[2], "images": []
                }

                cursor.execute("SELECT id, image_path FROM applicant_certificate_image WHERE certificate_id=?", (record[0],))
                images = cursor.fetchall()
                for img in images:
                    cer["images"].append({"id": img[0], "image_path": img[1]})

                all_certificate.append(cer)
            cursor.close()
            connection.close()

            return all_certificate
        except:
            raise

    def insert_applicant_certificate(self, applicant_id):
        try:
            connection = pyodbc.connect(CONNECTION_STRING)
            cursor = connection.cursor()
            cursor.execute("INSERT INTO applicant_certificate (applicant_id) VALUES (?)", (applicant_id, ))
            cursor.commit()
            cursor.execute("SELECT MAX(id) FROM applicant_certificate")
            id = cursor.fetchone()[0]
            cursor.close()
            connection.close()

            return id
        except:
            raise

    def update_applicant_certificate(self, id, name, received_date):
        try:
            received_date = None if not received_date else received_date
            connection = pyodbc.connect(CONNECTION_STRING)
            cursor = connection.cursor()
            cursor.execute("UPDATE applicant_certificate SET name=?, received_date=? WHERE id=?", (name, received_date, id))
            cursor.commit()
            cursor.close()
            connection.close()
        except:
            raise

    def delete_applicant_certificate(self, id):
        try:
            connection = pyodbc.connect(CONNECTION_STRING)
            cursor = connection.cursor()
            cursor.execute("DELETE FROM applicant_certificate_image WHERE certificate_id=?", (id, ))
            cursor.execute("DELETE FROM applicant_certificate WHERE id=?", (id, ))
            cursor.commit()
            cursor.close()
            connection.close()
        except:
            raise

    # applicant certificate image
    def insert_applicant_certificate_image(self, certificate_id, certificate_image_dir_path, extension):
        try:
            connection = pyodbc.connect(CONNECTION_STRING)
            cursor = connection.cursor()
            cursor.execute("INSERT INTO applicant_certificate_image(certificate_id) VALUES (?)", (certificate_id, ))
            cursor.commit()
            cursor.execute("SELECT MAX(id) FROM applicant_certificate_image")
            id = cursor.fetchone()[0]
            image_path = os.path.join(certificate_image_dir_path, str(id) + extension)
            cursor.execute("UPDATE applicant_certificate_image SET image_path=? WHERE id=?", (image_path, id))
            cursor.commit()
            cursor.close()
            connection.close()

            return id, image_path
        except:
            raise

    def delete_applicant_certificate_image(self, applicant_certificate_image_id):
        try:
            connection = pyodbc.connect(CONNECTION_STRING)
            cursor = connection.cursor()
            cursor.execute("SELECT image_path FROM applicant_certificate_image WHERE id=?", (applicant_certificate_image_id, ))
            image_path = cursor.fetchone()[0]
            cursor.execute("DELETE FROM applicant_certificate_image WHERE id=?", (applicant_certificate_image_id, ))
            cursor.commit()
            cursor.close()
            connection.close()
            return image_path
        except:
            raise

