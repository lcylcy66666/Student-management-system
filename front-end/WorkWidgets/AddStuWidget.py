import json
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QIntValidator
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent
from SocketClient.SocketClient import SocketClient

from SocketClient.ServiceController import ServiceController

class AddStuWidget(QtWidgets.QWidget):
    def __init__(self, client):
        super().__init__()
        self.setObjectName("add_stu_widget")
        self.client = client
        layout = QtWidgets.QGridLayout()
        header_label = LabelComponent(20, "Add Student")

        self.student_dict = {
            'name': "",
            'scores':"" 
        }

        #subject 暫存dictionary
        self.subject_dict = dict()

        '''左邊titile'''
        name_label = LabelComponent(16, "Name: ")
        subject_label = LabelComponent(16, "Subject:")
        score_label = LabelComponent(16, "Score:")
        
        '''中間輸入欄位'''
        self.editor_name = LineEditComponent()
        self.editor_name.setPlaceholderText("Name")
        self.editor_subject = LineEditComponent()
        self.editor_subject.setPlaceholderText("Subject")
        self.editor_score = LineEditComponent()
        
        '''強制只能輸入int'''
        self.editor_score.setValidator(QIntValidator())

        self.editor_subject.setEnabled(False)
        self.editor_score.setEnabled(False)

        '''event handler'''
        self.editor_name.mousePressEvent = self.clear_editor_content
        self.show_label = LabelComponent(16, "")
        self.show_label.setStyleSheet("color: red")


        '''button'''
        self.button_confirm = ButtonComponent("Confirm")
        self.button_Query = ButtonComponent("Query")
        self.button_add = ButtonComponent("Add")

        self.button_confirm.clicked.connect(self.confirm_action)        
        self.button_Query.clicked.connect(self.query_action)
        self.button_add.clicked.connect(self.add_action)

        '''layout_label'''
        layout.addWidget(header_label, 0, 0, 2, 4)
        layout.addWidget(name_label, 2, 0, 2, 2)
        layout.addWidget(subject_label, 4, 0, 2, 2)
        layout.addWidget(score_label, 6, 0, 2, 2)

        '''layout_edit'''
        layout.addWidget(self.editor_name, 2, 2, 1, 2)
        layout.addWidget(self.editor_subject, 4, 2, 1, 3)
        layout.addWidget(self.editor_score, 6, 2, 1, 3)

        '''layout_show'''
        layout.addWidget(self.show_label, 1, 6, 6, 5)
        
        '''layout_button'''
        layout.addWidget(self.button_Query, 2, 5, 1, 1)
        layout.addWidget(self.button_add, 5, 5, 4, 1)
        layout.addWidget(self.button_confirm, 7, 5, 3, 3)
        self.button_add.setEnabled(False)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 9)
        layout.setRowStretch(0, 2)
        layout.setRowStretch(1, 2)
        layout.setRowStretch(2, 2)
        layout.setRowStretch(3, 4)

        self.setLayout(layout)
    def load(self):
        pass

    def clear_editor_content(self, event):
        self.editor_name.clear()
        self.editor_subject.setEnabled(False)
        self.editor_score.setEnabled(False)
        self.button_add.setEnabled(False)

    def confirm_action(self):
        self.qthread = ServiceController(self.client, 'add', self.student_dict)
        self.qthread.start()

        if len(self.editor_subject.text())==0 or len(self.editor_score.text())==0:
            empty_hint = 'subject or score is empty or string.'
            self.show_label.setText(empty_hint)
        else:
            self.qthread.send_Msg.connect(self.receive_msg_add)


    def query_action(self, event):
        self.name = self.editor_name.text()
        '''initialize subject_dict'''
        self.subject_dict={}
        self.qthread = ServiceController(self.client, 'query', self.student_dict)
        self.qthread.start()

        if (self.name == ''):
            self.show_label.setText("Name can not be empty")
        else:
            self.student_dict['name']=self.name
            self.qthread.send_Msg.connect(self.receive_msg_query)
       
    def add_action(self, event):
        score = self.editor_score.text()
        subject = self.editor_subject.text()

        '''empty or score is string hint'''
        if len(subject)==0 or len(score) ==0 :
            empty_hint = 'subject or score is empty or string.'
            self.show_label.setText(empty_hint)
        else:
            add_success = "Student {}'s subject '{}' with score '{}' added".format(self.editor_name.text(), self.editor_subject.text(), self.editor_score.text())
            self.show_label.setText(add_success)
            
            self.subject_dict.update({subject: score})
            self.student_dict['scores'] = self.subject_dict
            self.button_confirm.setEnabled(True)
            
    '''when server send back msg to client, then display msg on window'''
    def receive_msg_query(self, value):
        self.show_label.setText(json.dumps(value))
        if (value['status'] == 'Fail'):
            self.button_add.setEnabled(False)
            self.button_confirm.setEnabled(False)
            self.editor_subject.setEnabled(False)
            self.editor_score.setEnabled(False)
        else:
            self.button_confirm.setEnabled(False)
            self.button_add.setEnabled(True)
            self.editor_subject.setEnabled(True)
            self.editor_score.setEnabled(True)

        
    def receive_msg_add(self, value):
       
        if (value['status'] =='OK'):
            self.show_label.setText("add {} successed.".format(self.student_dict))
        else:
            self.show_label.setText("ERROR.")

        self.editor_name.clear()                
        self.editor_subject.clear()
        self.editor_score.clear()

        self.editor_subject.setEnabled(False)
        self.editor_score.setEnabled(False)
        self.button_add.setEnabled(False)
    