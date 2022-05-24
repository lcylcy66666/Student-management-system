from DBController.StudentInfoTable import StudentInfoTable
from DBController.SubjectInfoTable import SubjectInfoTable
class QueryStu:
    def execute(self, message):
        try:
            
            '''Query要比對資料庫中是否有相同名字，如果有要提示錯誤'''
            #可以找到stu_id，找得到代表有，如果找不到回傳fail，代表可以新增
            if len(StudentInfoTable().select_a_student(message['name']))> 0:
                info = 'Fail'
                reason = 'The name is found, you can only modify or delete.'
                # print("Found")
            else:
                if message['name'] =='':
                    info = 'Fail'
                    reason = 'The name is empty, you must input student name.'
                else:
                    info ='OK'
                    reason = "You can input '{}''s subject and score now.".format(message['name'])
                # print("Not found")

            execution_result = {
                "status": info,
                'reason': reason
            }

            return execution_result
        except Exception as e:
            print(f"{e}")