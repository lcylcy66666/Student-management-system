from PyQt5 import QtWidgets, QtGui, QtCore
from WorkWidgets.AddStuWidget import AddStuWidget
from WorkWidgets.ShowStuWidget import ShowStuWidget
from WorkWidgets.ModifyStuWidget import ModifyStuWidget
from WorkWidgets.DelStuWidget import DelStuWidget
from WorkWidgets.WidgetComponents import LabelComponent
from WorkWidgets.WidgetComponents import ButtonComponent

from SocketClient.SocketClient import SocketClient

class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("main_widget")

        layout = QtWidgets.QGridLayout()
        header_label = LabelComponent(24, "Student Management System")
        host = "127.0.0.1"
        port = 20001
        BUFFER_SIZE = 1940
        client = SocketClient(host, port)
        function_widget = FunctionWidget(client)
        menu_widget = MenuWidget(function_widget.update_widget)

        layout.addWidget(header_label, 0, 0, 1, 2)
        layout.addWidget(menu_widget, 1, 0, 1, 1)
        layout.addWidget(function_widget, 1, 1, 1, 1)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 2)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 2)

        self.setLayout(layout)


class MenuWidget(QtWidgets.QWidget):
    def __init__(self, update_widget_callback):
        super().__init__()
        self.setObjectName("menu_widget")
        self.update_widget_callback = update_widget_callback

        layout = QtWidgets.QVBoxLayout()
        add_button = ButtonComponent("Add student")
        modify_button = ButtonComponent("Modify student")
        del_button = ButtonComponent("Del student")
        show_button = ButtonComponent("Show all")

        add_button.clicked.connect(lambda: self.update_widget_callback("add"))
        modify_button.clicked.connect(lambda: self.update_widget_callback("modify"))
        del_button.clicked.connect(lambda: self.update_widget_callback("del"))
        show_button.clicked.connect(lambda: self.update_widget_callback("show"))

        layout.addWidget(add_button, stretch=1)
        layout.addWidget(modify_button, stretch=1)
        layout.addWidget(del_button, stretch=1)
        layout.addWidget(show_button, stretch=1)

        self.setLayout(layout)


class FunctionWidget(QtWidgets.QStackedWidget):
    def __init__(self,client):
        super().__init__()
        self.client = client

        self.widget_dict = {
            "add": self.addWidget(AddStuWidget(self.client)),
            "modify": self.addWidget(ModifyStuWidget(self.client)),
            "del": self.addWidget(DelStuWidget(self.client)),
            "show": self.addWidget(ShowStuWidget(self.client))
        }
        self.update_widget("add")
    
    def update_widget(self, name):
        self.setCurrentIndex(self.widget_dict[name])
        current_widget = self.currentWidget()
        current_widget.load()
