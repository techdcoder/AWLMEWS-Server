from TestDialog import *
from InfoDialog import *
from SettingsDialog import *

class ControlPanelWindow(QtWidgets.QMainWindow):
    def __init__(self, socketHandler : SocketHandler, serverThread : QtCore.QThread):
        self.socketHandler = socketHandler
        self.serverThread = serverThread
        self.settings = Settings()
        self.settings.defaultSettings()

        super().__init__()

        self.mainWidget = QtWidgets.QWidget()
        self.mainLayout = QtWidgets.QVBoxLayout(self.mainWidget)

        self.testButton = QtWidgets.QPushButton("Test")
        self.settingsButton = QtWidgets.QPushButton("Settings")
        self.exitButton = QtWidgets.QPushButton("Exit")

        self.mainLayout.addWidget(self.testButton)
        self.testButton.clicked.connect(self.testButtonCallback)    
        
        self.mainLayout.addWidget(self.settingsButton)
        self.settingsButton.clicked.connect(self.settingsButtonCallback)

        self.mainLayout.addWidget(self.exitButton)
        self.exitButton.clicked.connect(self.exitButtonCallback)

        self.setCentralWidget(self.mainWidget)

    @QtCore.Slot()
    def testButtonCallback(self):
        filePath,description = InfoDialog().exec()
        TestDialog(self.socketHandler,filePath,description,self.settings).exec()

    @QtCore.Slot() 
    def settingsButtonCallback(self):
        SettingsDialog(self.settings, self.socketHandler).exec()

    @QtCore.Slot() 
    def exitButtonCallback(self):
        pass 
        