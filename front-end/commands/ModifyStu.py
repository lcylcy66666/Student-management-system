
import json

class ModifyStu():
    def __init__(self, client, select_result):
        self.client = client
        self.select_result = select_result
   
    def execute(self, dictionary) :
        
        send ={
            'name': dictionary['name'],
            'scores': dictionary['scores']
        }
        self.client.send_command(self.select_result, send)
        result = self.client.wait_response()
        result = json.loads(result)
        return result

    # def check(self, dictionary):
