from DBController.StudentInfoTable import StudentInfoTable
from DBController.SubjectInfoTable import SubjectInfoTable

class DelStu:
    
    def execute(self,parameters):
        name = parameters['name']
        subject_UI = parameters['subject']

        stu_id = StudentInfoTable().select_a_student(name)[0]
        subject_db = SubjectInfoTable().select_student_subject(stu_id)
        
        if stu_id:
            if subject_UI in subject_db:
                SubjectInfoTable().delete_student_subject(subject_UI)
                return {'status': "OK"}
            else:
                return {'status': 'False'}
        else:
            return {'status': 'False'}
        # StudentInfoTable().delete_a_student(stu_id)  
