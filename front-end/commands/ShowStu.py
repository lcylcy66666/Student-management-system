import imp


import json

class ShowStu():
    def __init__(self, client, select_result):
        self.client = client
        self.select_result = select_result
   
    def execute(self, dictionary):
        try: 
            self.client.send_command(self.select_result, dictionary)
            result = self.client.wait_response()
            
            result = json.loads(result)
            return result

        except Exception as e:
            print(f"{e}")