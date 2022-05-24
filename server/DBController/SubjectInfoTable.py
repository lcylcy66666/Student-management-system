from unittest import result
from DBController.DBConnection import DBConnection
from DBController.StudentInfoTable import StudentInfoTable

class SubjectInfoTable:
    def insert_a_subject(self, stu_id, subject, score):
        command = "INSERT INTO subject_info (stu_id, subject, score) VALUES  ('{}', '{}', '{}');".format(stu_id, subject, score)
            
        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()

    def select_student_subject(self, stu_id):
        command = "SELECT * FROM subject_info WHERE stu_id='{}';".format(stu_id)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            record_from_db = cursor.fetchall()

        return [row['subject'] for row in record_from_db]
        # result = dict()
        # for row in record_from_db:
        #     result[row['subject']] = row['score']
        # return result
    def select_all_subject(self, stu_id):
        command = "SELECT * FROM subject_info WHERE stu_id='{}';".format(stu_id)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            record_from_db = cursor.fetchall()

        result = dict()
        for row in record_from_db:
            result[row['subject']] = row['score']
        return result

    def delete_student_subject(self, subject):
        command = "DELETE FROM subject_info WHERE subject='{}';".format(subject)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()

    def delete_student_subjects(self, stu_id):
        command = "DELETE FROM subject_info WHERE stu_id='{}';".format(stu_id)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()

    def update_a_subject(self, stu_id, subject, score):
        command = "UPDATE subject_info SET score='{}' WHERE stu_id='{}' AND subject='{}';".format(score, stu_id, subject)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()


    def select_a_student(self, name):
        command = "SELECT * FROM student_info WHERE name='{}';".format(name)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            record_from_db = cursor.fetchall()

        return [row['stu_id'] for row in record_from_db]
    
    
       