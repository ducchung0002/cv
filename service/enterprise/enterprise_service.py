import pyodbc
from werkzeug.security import generate_password_hash, check_password_hash

from entity.enterprise import enterprise
from service import CONNECTION_STRING


class enterprise_service:
    def register(self, name, email,role, password):
        hashed_pass = generate_password_hash(password)
        try:
            connection = pyodbc.connect(CONNECTION_STRING)
            cursor = connection.cursor()
            cursor.execute("INSERT INTO enterprise(name) VALUES (?)", (name))
            cursor.execute('SELECT MAX(id) FROM enterprise')
            max_id = cursor.fetchone()[0]
            cursor.execute("INSERT INTO enterprise_admin(enterprise_id, name, email, role, password_hashed) VALUES (?,?,?,?,?)",
                           (max_id, name, email, role, hashed_pass))
            cursor.commit()
            cursor.close()
            connection.close()
        except:
            raise

    def valid_login(self, email, password):
        try:
            enterprise = self.get_enterprise_by_email(email)
            if enterprise and check_password_hash(enterprise.password_hashed, password):
                return enterprise
            return None
        except:
            raise

    def get_enterprise_by_id(self, id):
        try:
            connection = pyodbc.connect(CONNECTION_STRING)
            cursor = connection.cursor()
            cursor.execute('''
                SELECT id,avatar,A.name,introduction,homepage, email
                from enterprise as A

                join
                enterprise_admin as B
                on A.id = B.enterprise_id
                WHERE id = ?''',(id))
            record = cursor.fetchone()
            print(record)
            cursor.close()
            connection.close()

            if record:
                return enterprise(
                    app_json={"id": record[0], "avatar": record[1], "name": record[2], "introduction": record[3],
                              "homepage": record[4], "email": record[5]})
            return None

        except:
            raise

    def get_enterprise_by_email(self, email):
        try:
            connection = pyodbc.connect(CONNECTION_STRING)
            cursor = connection.cursor()
            cursor.execute(
                "SELECT name,email,password_hashed,role,enterprise_id  FROM enterprise_admin WHERE email = ?",
                (email,))
            record = cursor.fetchone()
            cursor.close()
            connection.close()
            if record:
                return enterprise(
                    app_json={"name": record[0],  "email": record[1],
                              "password_hashed": record[2], "role": record[3], "enterprise_id": record[4]})
            return None

        except:
            raise

    def update_profile(self, app_json):
        try:
            (name, phone, address, facebook, github,
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
                UPDATE enterprise 
                SET name=?,birthdate=?,gender=?,phone=?,address=?,facebook=?,github=?,
                self_introduction=?,education_school_name=?,education_major=?,education_school_start_date=?,
                education_school_end_date=?,internship_enterprise_name=?,internship_position=?,
                internship_start_date=?,internship_end_date=? 
                WHERE id=?
            """
            placeholder = (name, phone, address, facebook, github, self_introduction, education_school_name,
                           education_major, education_school_start_date, education_school_end_date, internship_enterprise_name,
                           internship_position, internship_start_date, internship_end_date, id)
            cursor.execute(sql, placeholder)
            cursor.commit()
            cursor.close()
            connection.close()
        except:
            raise

    def update_avatar(self, id, avatar):
        try:
            connection = pyodbc.connect(CONNECTION_STRING)
            cursor = connection.cursor()
            cursor.execute("UPDATE enterprise SET avatar=? WHERE id=?", (avatar, id))
            cursor.commit()
            cursor.close()
            connection.close()
        except:
            raise

    def get_enterprise_skill(self, id):
        try:
            connection = pyodbc.connect(CONNECTION_STRING)
            cursor = connection.cursor()
            sql = """
                SELECT enterprise_skill.id, skill_id, skill_type_id, experience_id
                FROM enterprise_skill 
                    JOIN skill ON enterprise_skill.skill_id = skill.id 
                WHERE enterprise_id=?
            """
            cursor.execute(sql, (id,))
            records = cursor.fetchall()
            cursor.close()
            connection.close()
            enterprise_skills = []
            for record in records:
                enterprise_skills.append({
                    "id": record[0],
                    "skill_id": record[1],
                    "skill_type_id": record[2],
                    "experience_id": record[3],
                })
            return enterprise_skills
        except:
            raise

    def delete_enterprise_skill(self, id):
        try:
            connection = pyodbc.connect(CONNECTION_STRING)
            cursor = connection.cursor()
            cursor.execute("DELETE FROM enterprise_skill WHERE id=?", (id,))
            cursor.commit()
            cursor.close()
            connection.close()
        except:
            raise

    def update_enterprise_skill(self, id, skill_id, experience_id):
        try:
            connection = pyodbc.connect(CONNECTION_STRING)
            cursor = connection.cursor()
            cursor.execute("UPDATE enterprise_skill SET skill_id=?, experience_id=? WHERE id=?", (skill_id, experience_id, id))
            cursor.commit()
            cursor.close()
            connection.close()
        except:
            raise