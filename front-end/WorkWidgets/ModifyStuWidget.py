from PyQt5 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent
from SocketClient.ServiceController import ServiceController
from PyQt5.QtWidgets import QMessageBox, QPushButton


class ModifyStuWidget(QtWidgets.QWidget):
    def __init__(self, client):
        super().__init__()
        self.setObjectName("modify_stu_widget")
        self.client = client
        self.student_dict={
            'name': '',
            'scores': ''
        }        
        layout = QtWidgets.QVBoxLayout()
        modify_widget = ModifyWidget(self.client, self.student_dict)
        topWidget = TopWidget(self.client, modify_widget, self.student_dict)

        header_label = LabelComponent(20, "Modify Student")
        layout.addWidget(header_label, stretch=1)
        layout.addWidget(topWidget,stretch = 1)
        layout.addWidget(modify_widget, stretch=3)
        
        self.setLayout(layout)
    
    def load(self):
        print("modify widget")


class ModifyWidget(QtWidgets.QWidget):
    def __init__(self, client, stu_dict):
        super().__init__()
        self.setObjectName("modify_stu_widget")
        self.client = client
        self.student_dict = stu_dict
        self.subject_dict={}
        self.topWidget = TopWidget(self.client, ModifyWidget, stu_dict)

        layout_t = QtWidgets.QGridLayout()
        self.radio_button_change = QtWidgets.QRadioButton('Change')
        self.radio_button_add = QtWidgets.QRadioButton('Add new')
        self.subject = LineEditComponent()
        self.subject.setPlaceholderText("Subject")
        self.score = LineEditComponent()
        self.score.setPlaceholderText("Score")
        self.confirm_btn = ButtonComponent('confirm')
        self.confirm_btn.clicked.connect(self.confirm_btn_clicked)


        self.radio_button_change.toggled.connect(self.radio_button_on_clicked)
        self.radio_button_add.toggled.connect(self.radio_button_on_clicked)

        '''初始狀態'''
        self.radio_button_status_change_off()

        layout_t.addWidget(self.radio_button_change, 0, 0)
        layout_t.addWidget(self.radio_button_add, 0, 2)
        layout_t.addWidget(self.subject, 4, 0)
        layout_t.addWidget(self.score, 4, 2)
        layout_t.addWidget(self.confirm_btn, 6, 4)
        self.setLayout(layout_t)

    

    def radio_button_status_change_off(self):
        self.radio_button_add.setEnabled(False)
        self.radio_button_change.setEnabled(False)
        self.subject.setDisabled(True)
        self.score.setDisabled(True)
        self.confirm_btn.setDisabled(True)

    def radio_button_status_change_on(self):
        self.radio_button_add.setEnabled(True)
        self.radio_button_change.setEnabled(True)
        self.subject.setDisabled(False)
        self.score.setDisabled(False)
        self.confirm_btn.setDisabled(False)

    def radio_button_on_clicked(self):
        selected_button = self.sender()
        if selected_button.isChecked():
            print("{}".format(selected_button.text()))

    def confirm_btn_clicked(self):
        
        name = self.topWidget.input_name.text()
        print(name)
        subject = self.subject.text()
        score = self.score.text()
        self.subject_dict={}
        self.subject_dict.update({subject:score})

        self.student_dict['scores'] = self.subject_dict
           
        self.qthread = ServiceController(self.client, 'modify', self.student_dict)
        self.qthread.start()

        if (subject == '' or score ==''):
            message = "subject or score can not be empty"
            QMessageBox.critical(self, 'HINT', message)
        else:
            self.qthread.send_Msg.connect(self.receive_msg_modify)

    def receive_msg_modify(self, message):
        print('msg from modify')
        if (message['status'] == 'OK'):
            hint = "Add subject:{}, score: {} successed.".format(self.subject.text(), self.score.text())
            QMessageBox.critical(self, 'HINT', hint)
            self.radio_button_status_change_off()

        else:
            hint ='Please try again'
            QMessageBox.critical(self, 'HINT', hint)
    

class TopWidget(QtWidgets.QWidget):
    def __init__(self, client, widget, stu_dict):
        super().__init__()
        self.setObjectName("TOP_widget")
        self.student_dict = stu_dict
        self.client = client
        self.modifyWidget = widget

        layout_inner = QtWidgets.QHBoxLayout(self)
        
        self.name = LabelComponent(20, 'Name: ')
        self.input_name = LineEditComponent()
        self.query_btn = QPushButton('Query', self)

        self.query_btn.clicked.connect(self.query_action)
        
        layout_inner.addWidget(self.name)
        layout_inner.addWidget(self.input_name)
        layout_inner.addWidget(self.query_btn)

        self.setLayout(layout_inner)

    def query_action(self, event):
        name = self.input_name.text()
        self.student_dict['name'] = name

        self.qthread = ServiceController(self.client, 'query', self.student_dict)
        self.qthread.start()

        if (name == ''):
            message = "Name can not be empty"
            QMessageBox.critical(self, 'HINT', message)
        else:
            self.qthread.send_Msg.connect(self.receive_msg_query)
    
    def receive_msg_query(self, message):
        print('msg from query')
        if (message['status'] == 'Fail'):
            hint = "Choose which step you want to use, add new one or modify score."
            QMessageBox.critical(self, 'HINT', hint)
            self.modifyWidget.radio_button_status_change_on()

        else:
            hint ='Please use Add student function'
            QMessageBox.critical(self, 'HINT', hint)

