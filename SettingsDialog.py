from PySide6 import QtWidgets, QtCore
from Settings import *
from SocketHandler import *
class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, settings : Settings, socketHandler : SocketHandler):
        super().__init__()
        self.settings = settings
        self.socketHandler = socketHandler

        self.mainLayout = QtWidgets.QGridLayout()
        self.rowLayout = QtWidgets.QVBoxLayout()

        self.ultrasonicFrame = QtWidgets.QFrame()
        self.ultrasonicLabel = QtWidgets.QLabel("Ultrasonic Settings")
        self.ultrasonicLayout = QtWidgets.QFormLayout(self.ultrasonicFrame)
        self.ultrasonicLayout.addWidget(self.ultrasonicLabel)

        self.ultrasonicSamplesInput = QtWidgets.QLineEdit(str(self.settings.ultraSonicSamples))
        self.ultrasonicLayout.addRow("Measurement per Sample: ", self.ultrasonicSamplesInput)

        self.tofFrame = QtWidgets.QFrame()
        self.tofLayout = QtWidgets.QFormLayout(self.tofFrame)
        self.tofLabel = QtWidgets.QLabel("TOF Settings")
        self.tofLayout.addWidget(self.tofLabel)

        self.tofSamplesInput = QtWidgets.QLineEdit(str(self.settings.tofSamples))
        self.tofLayout.addRow("Measurement per Sample: ", self.tofSamplesInput)

        self.tofSignalRateLimitInput = QtWidgets.QLineEdit(str(self.settings.tofSignalRateLimit))
        self.tofLayout.addRow("Signal Rate Limit: ", self.tofSignalRateLimitInput)

        self.tofTimingBudgetInput = QtWidgets.QLineEdit(str(self.settings.tofTimingBudget))
        self.tofLayout.addRow("Timing Budget: ", self.tofTimingBudgetInput)

        self.rowLayout.addWidget(self.ultrasonicFrame)
        self.rowLayout.addWidget(self.tofFrame)

        self.mainLayout.addLayout(self.rowLayout,0,0,2,2)

        self.cancelButton = QtWidgets.QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.cancelCallback)
        self.mainLayout.addWidget(self.cancelButton,2,0,1,1)

        self.doneButton = QtWidgets.QPushButton("Done")
        self.doneButton.clicked.connect(self.doneCallback)
        self.mainLayout.addWidget(self.doneButton,2,1,1,1)

        self.setLayout(self.mainLayout)

    def saveSettings(self):
        self.settings.tofSamples = int(self.tofSamplesInput.text())
        self.settings.ultraSonicSamples = int(self.ultrasonicSamplesInput.text())

        self.settings.tofSignalRateLimit = float(self.tofSignalRateLimitInput.text())
        self.settings.tofTimingBudget = int(self.tofTimingBudgetInput.text())

    @QtCore.Slot()
    def doneCallback(self):
        self.saveSettings()
        self.socketHandler.updateSettings.emit(self.settings)
        self.close()

    @QtCore.Slot()
    def cancelCallback(self):
        self.close()
    def exec(self):
        super().exec()
        return self.settings
