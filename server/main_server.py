from SocketServer.SocketServer import SocketServer

from Commands.AddStu import AddStu
from Commands.PrintAll import PrintAll
from Commands.QueryStu import QueryStu
from Commands.DelStu import DelStu
from Commands.ModifyStu import Modify

from DBController.DBConnection import DBConnection
from DBController.DBInitializer import DBInitializer

action_list = {
        "add": AddStu, 
        "query": QueryStu,
        "show": PrintAll,
        "del": DelStu,
        "modify": Modify
    }

class management:
   
    def execute(self, message):
        command = message['command']
        parameters = message['parameters']
        reply_msg = action_list[command]().execute(parameters)
        return reply_msg
        
   
def main():

    DBConnection.db_file_path = "example.db"
    DBInitializer().execute()
    
    host = "127.0.0.1"
    port = 20001

    server = SocketServer(host, port, management())
    server.setDaemon=True
    server.serve()

    # because we set daemon is true, so the main thread has to keep alive
    while True:
        command = input()
        if command == "finish":
            break
    
    
    server.server_socket.close()
    print("leaving ....... ")

main()