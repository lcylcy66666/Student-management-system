from DBController.StudentInfoTable import StudentInfoTable
from DBController.SubjectInfoTable import SubjectInfoTable


class PrintAll:
    def __init__(self): 
        self.stu_list = []

    def execute(self, message):
        stu_ids = StudentInfoTable.select_all_student(self)
        # print(stu_ids)
        for stu_id, name in stu_ids.items():
            # print(stu_id, name)
            tmp = {
                'name':name, 
                'scores':SubjectInfoTable.select_all_subject(self,stu_id)
            }
            self.stu_list.append(tmp)

        print(self.stu_list)
        return {"status":"OK", "parameters":self.stu_list}
 