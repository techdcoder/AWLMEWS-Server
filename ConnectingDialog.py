from PySide6 import QtWidgets
from SocketHandler import *

class ConnectingDialog(QtWidgets.QDialog):
    def __init__(self, socketHandler):
        super().__init__()

        self.mainLayout = QtWidgets.QGridLayout() 
        self.formLayout = QtWidgets.QFormLayout()

        self.ipLabel = QtWidgets.QLabel(socketHandler.ipv4)
        self.portLabel = QtWidgets.QLabel(str(socketHandler.port))

        self.cancelButton = QtWidgets.QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.cancelButtonCallback)

        self.formLayout.addRow("IP: ", self.ipLabel)
        self.formLayout.addRow("Port: ",self.portLabel)

        self.mainLayout.addLayout(self.formLayout,0,0,2,1)
        self.mainLayout.addWidget(self.cancelButton,2,0,1,1)

        self.socketHandler = socketHandler
        socketHandler.connected.connect(self.close)

        self.setLayout(self.mainLayout)


    @QtCore.Slot()
    def cancelButtonCallback(self):
        self.socketHandler.close()
        self.close()