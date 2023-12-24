import traceback

import pyodbc
import os
import json
import smtplib
import threading

from werkzeug.security import generate_password_hash, check_password_hash
from entity.applicant import applicant
from service import CONNECTION_STRING
from email.mime.text import MIMEText
from random import randint, choice
from string import ascii_letters, digits, punctuation
from datetime import datetime, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # service/applicant/
RESET_PASSWORD_DIR = os.path.join(SCRIPT_DIR, "reset_password")


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
                "SELECT id,avatar_path,name,birthdate,gender,phone,address,email,password_hashed,facebook,github,self_introduction,education_school_name,education_major,education_school_start_date,education_school_end_date,internship_enterprise_name,internship_position,internship_start_date,internship_end_date  FROM applicant WHERE id=?",
                (id,))
            record = cursor.fetchone()
            cursor.close()
            connection.close()

            if record:
                return applicant(
                    app_json={"id": record[0], "avatar_path": record[1], "name": record[2], "birthdate": record[3],
                              "gender": record[4], "phone": record[5], "address": record[6], "email": record[7],
                              "password_hashed": record[8], "facebook": record[9], "github": record[10],
                              "self_introduction": record[11], "education_school_name": record[12],
                              "education_major": record[13], "education_school_start_date": record[14],
                              "education_school_end_date": record[15], "internship_enterprise_name": record[16],
                              "internship_position": record[17], "internship_start_date": record[18],
                              "internship_end_date": record[19]})
            return None
        except:
            raise

    def get_applicant_by_email(self, email):
        try:
            connection = pyodbc.connect(CONNECTION_STRING)
            cursor = connection.cursor()
            cursor.execute(
                "SELECT id,avatar_path,name,birthdate,gender,phone,address,email,password_hashed,facebook,github,self_introduction,education_school_name,education_major,education_school_start_date,education_school_end_date,internship_enterprise_name,internship_position,internship_start_date,internship_end_date  FROM applicant WHERE email=?",
                (email,))
            record = cursor.fetchone()
            cursor.close()
            connection.close()
            if record:
                return applicant(
                    app_json={"id": record[0], "avatar_path": record[1], "name": record[2], "birthdate": record[3],
                              "gender": record[4], "phone": record[5], "address": record[6], "email": record[7],
                              "password_hashed": record[8], "facebook": record[9], "github": record[10],
                              "self_introduction": record[11], "education_school_name": record[12],
                              "education_major": record[13], "education_school_start_date": record[14],
                              "education_school_end_date": record[15], "internship_enterprise_name": record[16],
                              "internship_position": record[17], "internship_start_date": record[18],
                              "internship_end_date": record[19]})
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
            placeholder = (
                name, birthdate, gender, phone, address, facebook, github, self_introduction, education_school_name,
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
            cursor.execute("UPDATE applicant_skill SET skill_id=?, experience_id=? WHERE id=?",
                           (skill_id, experience_id, id))
            cursor.commit()
            cursor.close()
            connection.close()
        except:
            raise

    def insert_applicant_skill(self, id, skill_id, experience_id):
        try:
            connection = pyodbc.connect(CONNECTION_STRING)
            cursor = connection.cursor()
            cursor.execute("INSERT INTO applicant_skill(applicant_id, skill_id, experience_id) VALUES(?, ?, ?)",
                           (id, skill_id, experience_id))
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
            cursor.execute("SELECT id, name, received_date FROM applicant_certificate WHERE applicant_id=?",
                           (applicant_id,))
            records = cursor.fetchall()
            all_certificate = []
            for record in records:
                cer = {
                    "id": record[0], "name": record[1],
                    "received_date": record[2], "images": []
                }

                cursor.execute("SELECT id, image_path FROM applicant_certificate_image WHERE certificate_id=?",
                               (record[0],))
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
            cursor.execute("INSERT INTO applicant_certificate (applicant_id) VALUES (?)", (applicant_id,))
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
            cursor.execute("UPDATE applicant_certificate SET name=?, received_date=? WHERE id=?",
                           (name, received_date, id))
            cursor.commit()
            cursor.close()
            connection.close()
        except:
            raise

    def delete_applicant_certificate(self, id):
        try:
            connection = pyodbc.connect(CONNECTION_STRING)
            cursor = connection.cursor()
            cursor.execute("DELETE FROM applicant_certificate_image WHERE certificate_id=?", (id,))
            cursor.execute("DELETE FROM applicant_certificate WHERE id=?", (id,))
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
            cursor.execute("INSERT INTO applicant_certificate_image(certificate_id) VALUES (?)", (certificate_id,))
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
            cursor.execute("SELECT image_path FROM applicant_certificate_image WHERE id=?",
                           (applicant_certificate_image_id,))
            image_path = cursor.fetchone()[0]
            cursor.execute("DELETE FROM applicant_certificate_image WHERE id=?", (applicant_certificate_image_id,))
            cursor.commit()
            cursor.close()
            connection.close()
            return image_path
        except:
            raise

    # password service
    def send_email(self, mail_msg, mail_subject, mail_from, mail_to, mail_user="ducchung2444@gmail.com", mail_app_password="fymizjaxqsrqfjzb"):
        msg = MIMEText(mail_msg)
        msg["Subject"] = mail_subject
        msg["From"] = mail_from
        msg["To"] = mail_to

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
                smtp.starttls()
                smtp.login(mail_user, mail_app_password)
                smtp.send_message(msg)
        except:
            raise

    def send_verify_code(self, email):
        recovery_code = ""
        for _ in range(6):
            recovery_code += str(randint(0, 9))

        save_file_path = os.path.join(RESET_PASSWORD_DIR, email + ".txt")
        if os.path.isfile(save_file_path):
            with open(save_file_path, 'r') as file:
                try:
                    reset_password_token = json.loads(file.read())
                    request_time = datetime.strptime(reset_password_token["request_time"], "%Y-%m-%d %H:%M:%S.%f")
                    current_time = datetime.now()
                    time_difference = current_time - request_time

                    # Make sure this request with last request difference larger than 50 seconds
                    if time_difference.total_seconds() < 30:
                        return False
                except:
                    pass

        request_time = datetime.now()
        request_time_to_str = request_time.strftime("%Y-%m-%d %H:%M:%S.%f")

        reset_password_token = {
            "recovery_code": recovery_code,
            "request_time": request_time_to_str
        }

        with open(save_file_path, 'w') as file:
            file.write(json.dumps(reset_password_token))

        mail_msg = f"Mã khôi phục mật khẩu của bạn là {recovery_code}. Mã này chỉ có hiệu lực trong vòng 2 phút."
        mail_subject = "Mã khôi phục mật khẩu"
        mail_from = "ducchung2444@gmail.com"
        mail_to = email

        thread = threading.Thread(target=self.send_email, args=(mail_msg, mail_subject, mail_from, mail_to))
        thread.start()

        return True

    def check_recovery_code(self, email, recovery_code):
        save_file_path = os.path.join(RESET_PASSWORD_DIR, email + ".txt")
        if os.path.exists(save_file_path):
            with open(save_file_path, 'r') as file:
                reset_password_token = json.loads(file.read())

            if recovery_code != reset_password_token["recovery_code"]:
                return False
            current_time = datetime.now()
            request_time = datetime.strptime(reset_password_token["request_time"], "%Y-%m-%d %H:%M:%S.%f")
            time_difference = current_time - request_time

            if time_difference.total_seconds() > 2 * 60:
                return False

            os.remove(save_file_path)
            return True
        else:
            return False

    def reset_password(self, email, recovery_code):
        if not self.check_recovery_code(email, recovery_code):
            return False
        length = 12
        random_password = ''.join(choice(ascii_letters + digits) for _ in range(length))
        self.change_password(email, random_password)
        # create thread to sending new password to email

        mail_msg = f"Hệ thống đã đặt lại mật khẩu mới cho bạn. Mật khẩu mới là: {random_password}"
        mail_subject = "Mật khẩu đặt lại"
        mail_from = "ducchung2444@gmail.com"
        mail_to = email

        thread = threading.Thread(target=self.send_email, args=(mail_msg, mail_subject, mail_from, mail_to))
        thread.start()

        return True

    def change_password(self, email, new_password):
        password_hashed = generate_password_hash(new_password)
        try:
            connection = pyodbc.connect(CONNECTION_STRING)
            cursor = connection.cursor()
            cursor.execute("UPDATE applicant SET password_hashed=? WHERE email=?",
                           (password_hashed, email))
            cursor.commit()
            cursor.close()
            connection.close()
            return True
        except:
            raise

    def check_password(self, pwhash, password):
        return check_password_hash(pwhash, password)

    # application
    def get_all_application(self):
        try:
            connection = pyodbc.connect(CONNECTION_STRING)
            cursor = connection.cursor()
            cursor.execute("UPDATE applicant SET password_hashed=? WHERE email=?",
                           (password_hashed, email))
            cursor.commit()
            cursor.close()
            connection.close()
            return True
        except:
            raise