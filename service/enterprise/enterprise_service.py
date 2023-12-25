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
                SELECT id,avatar,A.name,introduction,homepage, email, role
                from enterprise as A
                join
                enterprise_admin as B
                on A.id = B.enterprise_id
                WHERE id = ?''',(id))
            record = cursor.fetchone()
            cursor.close()
            connection.close()
            print("Record", record)
            if record:
                return enterprise(
                    app_json={"enterprise_id": record[0], "avatar": record[1], "name": record[2], "introduction": record[3],
                              "homepage": record[4], "email": record[5], "role":record[6]})
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
            (name, introduction,homepage, enterprise_id) = (
                app_json["name"],  app_json["introduction"], app_json["homepage"],app_json["enterprise_id"])

            name = None if not name else name
            introduction = None if not introduction else introduction
            homepage = None if not homepage else homepage
            enterprise_id = None if not enterprise_id else enterprise_id
            connection = pyodbc.connect(CONNECTION_STRING)
            cursor = connection.cursor()
            sql = """
                UPDATE enterprise 
                SET name=?,introduction=?,homepage=?
                WHERE id=?
            """
            placeholder = (name, introduction, homepage,enterprise_id)
            cursor.execute(sql, placeholder)
            print("sql", sql)
            cursor.commit()
            cursor.close()
            connection.close()
        except:
            raise
    def add_recruitment(self, app_json):
        try:
            jobName = app_json["jobName"];
            jobDescription = app_json["jobDescription"];
            position = app_json["position"];
            applicantRequirement = app_json["applicantRequirement"];
            benefit = app_json["benefit"];
            minSalary = app_json["minSalary"];
            maxSalary = app_json["maxSalary"];
            deadline = app_json["deadline"];
            postDate = app_json["postDate"];
            enterprise_id = app_json["enterprise_id"]
            jobName = None if not jobName else jobName
            jobDescription = None if not jobDescription else jobDescription
            position = None if not position else position
            applicantRequirement = None if not applicantRequirement else applicantRequirement
            benefit = None if not benefit else benefit
            minSalary = None if not minSalary else minSalary
            maxSalary = None if not maxSalary else maxSalary
            deadline = None if not deadline else deadline
            postDate = None if not postDate else postDate
            enterprise_id =  None if not enterprise_id else enterprise_id
            connection = pyodbc.connect(CONNECTION_STRING)
            cursor = connection.cursor()
            sql = """
                INSERT INTO recruiment(job_name, job_description, position, applicant_requirement, benefit, min_salary, max_salary, enterprise_id, deadline, postdate)
                VALUES (?,?,?,?,?,?,?,?,?,?)
            """
            placeholder = (jobName, jobDescription, position, applicantRequirement, benefit, minSalary, maxSalary, enterprise_id, deadline, postDate)
            
            cursor.execute(sql, placeholder)
            print("sql", sql)
            cursor.commit()
            cursor.close()
            connection.close()
        except : 
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
        
    def get_all_enterprises(self):
        try:
            connection = pyodbc.connect(CONNECTION_STRING)
            cursor = connection.cursor()
            cursor.execute('SELECT id, name FROM enterprise')  # Chọn các trường bạn muốn lấy từ bảng enterprise
            records = cursor.fetchall()
            cursor.close()
            connection.close()

            enterprises = []
            for record in records:
                enterprises.append({
                    "id": record[0],
                    "name": record[1],
                    # Bổ sung các trường thông tin khác nếu cần thiết
                })
            return enterprises
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
        