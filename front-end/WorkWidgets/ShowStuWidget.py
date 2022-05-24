from cProfile import label
from PyQt5 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent
from SocketClient.ServiceController import ServiceController
import json

class ShowStuWidget(QtWidgets.QWidget):
    def __init__(self, client):
        super().__init__()
        self.setObjectName("show_stu_widget")
        self.client = client
        self.show_label = LabelComponent(16, "")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.header_label = LabelComponent(20, "Show Student")
        self.layout.addWidget(self.header_label, stretch=0)

        self.title = LabelComponent(20, '==== Stuednt List =====')
        
        self.show_3 = LabelComponent(10, '')

        '''最底層放student_list的layout'''
        self.QVBoxLayout = QtWidgets.QVBoxLayout()
        self.widget = QtWidgets.QWidget()                 # Widget that contains the collection of Vertical Box

        self.scroll = QtWidgets.QScrollArea()        
        self.scroll.setLayout(self.QVBoxLayout)
        self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.layout.addWidget(self.scroll, stretch=0)
        self.setLayout(self.layout)

    def load(self):
        print('Load_show')
        for i in reversed(range(self.QVBoxLayout.count())): 
            self.QVBoxLayout.itemAt(i).widget().setParent(None)        
            
        self.qthread = ServiceController(self.client, 'show', {})
        self.qthread.start()           
        self.qthread.send_Msg.connect(self.receive_msg_show)

    def receive_msg_show(self, value):
        # value = json.dumps(value)
        self.QVBoxLayout.addWidget(self.title)
        for para in value['parameters']:
            self.QVBoxLayout.addWidget(LabelComponent(15, "Name: {}".format(para['name'])))
            for subject, score in para['scores'].items():
                self.QVBoxLayout.addWidget(LabelComponent(15, "Subject: {}, score: {}".format(subject, score)))              
        self.QVBoxLayout.addWidget(LabelComponent(20, '============='))
        self.widget.setLayout(self.QVBoxLayout)