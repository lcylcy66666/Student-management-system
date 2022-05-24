import json
from commands.QueryStu import QueryStu

class AddStu:
    def __init__(self, client, select_result):
        self.client = client
        self.select_result = select_result

    def execute(self, dic):    
        try: 
            self.client.send_command(self.select_result, dic)
            result = self.client.wait_response()
            
            result = json.loads(result)
            return result

        except Exception as e:
            print(f"{e}")
    










