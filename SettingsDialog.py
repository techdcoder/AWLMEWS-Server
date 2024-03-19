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

        self.generalFrame = QtWidgets.QFrame()
        self.generalLayout = QtWidgets.QFormLayout(self.generalFrame)
        self.generalLabel = QtWidgets.QLabel("General Settings")
        self.generalLayout.addWidget(self.generalLabel)

        self.prototypeHeightInput = QtWidgets.QLineEdit(str(self.settings.prototypeHeight))
        self.generalLayout.addRow("Prototype Height: ", self.prototypeHeightInput)

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

        self.demoFrame = QtWidgets.QFrame()
        self.demoLayout = QtWidgets.QFormLayout(self.demoFrame)

        self.demoLabel = QtWidgets.QLabel("Demo Settings")
        self.demoLayout.addWidget(self.demoLabel)

        self.thresholdInput = QtWidgets.QLineEdit(str(self.settings.threshold))
        self.demoLayout.addRow("Threshold: ", self.thresholdInput)

        self.iotCheckbox = QtWidgets.QCheckBox()
        self.iotCheckbox.setChecked(self.settings.iotEnabled)

        self.facebookCheckbox = QtWidgets.QCheckBox()
        self.facebookCheckbox.setChecked(self.settings.facebookEnabled)

        self.sirenCheckbox = QtWidgets.QCheckBox()
        self.sirenCheckbox.setChecked(self.settings.sirenEnabled)

        self.demoLayout.addRow("IOT: ", self.iotCheckbox)
        self.demoLayout.addRow("Facebook: ", self.facebookCheckbox)
        self.demoLayout.addRow("Siren: ", self.sirenCheckbox)

        self.rowLayout.addWidget(self.generalFrame)
        self.rowLayout.addWidget(self.ultrasonicFrame)
        self.rowLayout.addWidget(self.tofFrame)
        self.rowLayout.addWidget(self.demoFrame)

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

        self.settings.prototypeHeight = float(self.prototypeHeightInput.text())

        self.settings.iotEnabled = self.iotCheckbox.isChecked()
        self.settings.facebookEnabled = self.facebookCheckbox.isChecked()
        self.settings.sirenEnabled = self.sirenCheckbox.isChecked()

        self.settings.threshold = float(self.thresholdInput.text())

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
