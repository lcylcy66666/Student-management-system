from WorkWidgets.MainWidget import MainWidget
from PyQt5.QtWidgets import QApplication
from PyQt5 import sip
import sys
from SocketClient.SocketClient import SocketClient

app = QApplication([])
main_window = MainWidget()


main_window.setFixedSize(700, 300)
main_window.show()
# main_window.showFullScreen()

sys.exit(app.exec_())
