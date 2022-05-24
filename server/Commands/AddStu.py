from DBController.SubjectInfoTable import SubjectInfoTable
from DBController.StudentInfoTable import StudentInfoTable

class AddStu:
    def execute(self, message):

        try:
            StudentInfoTable().insert_a_student(message['name'])
            stu_id = StudentInfoTable().select_a_student(message['name'])[0]
            
            for subject, score in message['scores'].items():
                SubjectInfoTable().insert_a_subject(stu_id, subject, score)
            
            execution_result = {
                "status": "OK"
            }
            return execution_result

        except Exception as e:
            print(f"{e}")
        
                    