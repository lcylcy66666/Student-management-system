
from email import message
from PyQt5 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent
from SocketClient.ServiceController import ServiceController
from PyQt5.QtWidgets import QMessageBox, QPushButton


class DelStuWidget(QtWidgets.QWidget):
    def __init__(self, client):
        super().__init__()
        self.setObjectName("modify_stu_widget")
        self.client = client

        layout = QtWidgets.QVBoxLayout()
        del_widget = DelWidget(self.client)

        header_label = LabelComponent(20, "Delete Student")
        
        layout.addWidget(header_label, stretch=1)
        layout.addWidget(del_widget, stretch=5)
        self.setLayout(layout)

    def load(self):
        print("Del widget")
    

class DelWidget(QtWidgets.QWidget):
    def __init__(self, client):
        super().__init__()
        self.setObjectName("delete_stu_widget")
        self.client = client
        self.student_dict = {}

        layout = QtWidgets.QVBoxLayout()

        self.editor_name = LineEditComponent()
        self.editor_name.setPlaceholderText("Name")
        self.editor_subject = LineEditComponent()
        self.editor_subject.setPlaceholderText("Subject")

        # confirm_button = ButtonComponent('Confirm_del')
        confirm_button = QPushButton('Confirm', self)
        confirm_button.clicked.connect(self.button_confirm)
        name_label = LabelComponent(16, "Name")
        subject_label = LabelComponent(16, "Subject")

        layout.addWidget(name_label)
        layout.addWidget(self.editor_name)
        layout.addWidget(subject_label)
        layout.addWidget(self.editor_subject)
        layout.addWidget(confirm_button)

        self.setLayout(layout)

    def combo_box_select_changed(self, index):
        print ("Index {} {} selected".format(index, self.combo_box_name.currentText()))

    def button_confirm(self):
        name = self.editor_name.text()
        subject = self.editor_subject.text()
        self.student_dict = {
            'name': name,
            'subject': subject
        }

        self.qthread = ServiceController(self.client, 'del', self.student_dict)
        self.qthread.start()

        if len(self.editor_subject.text())==0:
            empty_hint = 'Subject is empty, will not be execute!'
            QMessageBox.critical(self, 'HINT', empty_hint)
        else:
            self.qthread.send_Msg.connect(self.receive_msg_del)

    def receive_msg_del(self, message):
        # print(message+'receive from function')
        if(message['status'] == 'OK'):
            message = "Del success!"
            QMessageBox.critical(self, 'HINT', message)

        else:
            message = "ERROR! Name not found or subject is not exist!"
            QMessageBox.critical(self, 'HINT', message)


    