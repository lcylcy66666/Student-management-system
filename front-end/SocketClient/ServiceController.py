from PyQt5.QtCore import QThread, pyqtSignal
from commands.AddStu import AddStu
from commands.DelStu import DelStu
from commands.ModifyStu import ModifyStu
from commands.QueryStu import QueryStu
from commands.ShowStu import ShowStu

import json

class ServiceController(QThread):
    send_Msg = pyqtSignal(dict)

    def __init__(self, client, command, dictionary):
        super().__init__()
        self.client = client
        self.command = command
        self.dicitonary = dictionary
       
        self.action_list = {
            "add": AddStu, 
            "query": QueryStu,
            "show": ShowStu,
            "del": DelStu,
            "modify": ModifyStu
        }

    def run(self):
        try:
            result = self.action_list[self.command](self.client, self.command).execute(self.dicitonary)
            # print(type(result))
            self.send_Msg.emit(result)
            
        except Exception as e:
            print(f"{e}")

 


   
