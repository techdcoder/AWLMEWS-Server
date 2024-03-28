from TestDialog import *
from InfoDialog import *
from SettingsDialog import *
from DemoWindow import *

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
        self.demoButton = QtWidgets.QPushButton("Demo")
        self.settingsButton = QtWidgets.QPushButton("Settings")
        self.syncTimeButton = QtWidgets.QPushButton("Sync Time")
        self.exitButton = QtWidgets.QPushButton("Exit")

        self.mainLayout.addWidget(self.testButton)
        self.testButton.clicked.connect(self.testButtonCallback)    

        self.mainLayout.addWidget(self.demoButton)
        self.demoButton.clicked.connect(self.demoButtonCallback)

        self.mainLayout.addWidget(self.settingsButton)
        self.settingsButton.clicked.connect(self.settingsButtonCallback)

        self.mainLayout.addWidget(self.syncTimeButton)
        self.syncTimeButton.clicked.connect(self.syncTimeButtonCallback)

        self.mainLayout.addWidget(self.exitButton)
        self.exitButton.clicked.connect(self.exitButtonCallback)

        self.setCentralWidget(self.mainWidget)

    @QtCore.Slot()
    def testButtonCallback(self):
        filePath,description = InfoDialog().exec()
        TestDialog(self.socketHandler,filePath,description,self.settings).exec()

    @QtCore.Slot()
    def demoButtonCallback(self):
        self.demoWindow = DemoWindow(self, self.socketHandler)
        self.demoWindow.show()
        self.hide()

    @QtCore.Slot() 
    def settingsButtonCallback(self):
        SettingsDialog(self.settings, self.socketHandler).exec()

    def syncTimeButtonCallback(self):
        self.socketHandler.updateTime.emit()

    @QtCore.Slot() 
    def exitButtonCallback(self):
        self.close()
