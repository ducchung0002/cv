import pyodbc

from service import CONNECTION_STRING
from entity.skill_type import skill_type
from entity.skill import skill
from entity.experience import experience
class db_service:
    def get_all_skill_type(self):
        connection = pyodbc.connect(CONNECTION_STRING)
        cursor = connection.cursor()
        cursor.execute("SELECT id, name FROM skill_type")
        records = cursor.fetchall()
        cursor.close()
        connection.close()
        all_skill_type = []
        for record in records:
            all_skill_type.append({
                "id": record[0],
                "name": record[1]
            })
        return all_skill_type

    def get_all_skill(self):
        connection = pyodbc.connect(CONNECTION_STRING)
        cursor = connection.cursor()
        cursor.execute("SELECT id, skill_type_id, name FROM skill")
        records = cursor.fetchall()
        cursor.close()
        connection.close()
        all_skill = []
        for record in records:
            all_skill.append({
                "id": record[0],
                "skill_type_id": record[1],
                "name": record[2]
            })
        return all_skill

    def get_all_experience(self):
        connection = pyodbc.connect(CONNECTION_STRING)
        cursor = connection.cursor()
        cursor.execute("SELECT id, name FROM experience")
        records = cursor.fetchall()
        cursor.close()
        connection.close()
        all_experience = []
        for record in records:
            all_experience.append({
                "id": record[0],
                "name": record[1]
            })
        return all_experience

