from ConnectingDialog import *
from ControlPanelWindow import *

class StartupWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.serverThread = QtCore.QThread()

        self.mainWidget = QtWidgets.QWidget()

        self.mainLayout = QtWidgets.QGridLayout(self.mainWidget) 
        self.formLayout = QtWidgets.QFormLayout()

        self.portInput =  QtWidgets.QLineEdit("3600")
        self.formLayout.addRow("Port: ",self.portInput)

        self.mainLayout.addLayout(self.formLayout,0,0,2,1)  

        self.startButton = QtWidgets.QPushButton("Start")
        self.startButton.clicked.connect(self.startButtonCallback)
        self.mainLayout.addWidget(self.startButton,2,0,1,1)

        self.setCentralWidget(self.mainWidget)

    @QtCore.Slot()
    def startButtonCallback(self):
        self.socketHandler = SocketHandler(int(self.portInput.text()))
        self.socketHandler.moveToThread(self.serverThread)
        self.socketHandler.connected.connect(self.startControlPanelWindow)
        self.startServer.connect(self.socketHandler.waitConnection)
        self.serverThread.start()

        self.startServer.emit()

        ConnectingDialog(self.socketHandler).exec()
        
    @QtCore.Slot() 
    def startControlPanelWindow(self):
        self.hide()
        self.controlPanelWindow = ControlPanelWindow(self.socketHandler,self.serverThread)
        self.controlPanelWindow.show()

    startServer = QtCore.Signal()