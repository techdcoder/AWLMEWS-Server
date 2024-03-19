from PySide6 import QtWidgets
from SettingsDialog import *
from SocketHandler import *

class DemoWindow(QtWidgets.QMainWindow):
    def __init__(self, parentWindow : QtWidgets.QMainWindow, socketHandler : SocketHandler):
        super().__init__()
        self.parentWindow = parentWindow
        self.socketHandler = socketHandler
        self.socketHandler.beginDemoMode.emit()

        self.mainWidget = QtWidgets.QWidget()
        self.mainLayout = QtWidgets.QGridLayout(self.mainWidget)

        self.formLayout = QtWidgets.QFormLayout()
        self.ultrasonicReadingLabel = QtWidgets.QLabel()
        self.tofReadingLabel =  QtWidgets.QLabel()

        self.formLayout.addRow("Ultrasonic Reading: ", self.ultrasonicReadingLabel)
        self.formLayout.addRow("TOF Reading: ", self.tofReadingLabel)

        self.mainLayout.addLayout(self.formLayout,0,0,2,2)

        self.setCentralWidget(self.mainWidget)

        self.socketHandler.demoModeUpdated.connect(self.update)
    @QtCore.Slot()
    def update(self, ultrasonicWaterLevel : float, tofWaterLevel : float):
        self.ultrasonicReadingLabel.setText(str(ultrasonicWaterLevel))
        self.tofReadingLabel.setText(str(tofWaterLevel))

    def closeEvent(self, args):
        self.socketHandler.demoMode = False
        self.socketHandler.terminateDemoMode()
        self.parentWindow.show()
