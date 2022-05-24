from DBController.StudentInfoTable import StudentInfoTable
from DBController.SubjectInfoTable import SubjectInfoTable

class Modify:

    def execute(self,parameters) :
        name = parameters['name']
        stu_id = StudentInfoTable().select_a_student(name)[0]
        server_subject=SubjectInfoTable().select_all_subject(stu_id)
        for subject, score in parameters['scores'].items():
            if(subject in server_subject.keys()):
                SubjectInfoTable().update_a_subject(stu_id, subject, score)
                return {'status':'OK'}
            else:
                SubjectInfoTable().insert_a_subject(stu_id, subject, score)    
                return {'status':'OK'}

        return{'status': "Fail"}
        # return {'status':'OK'}