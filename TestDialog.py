from SocketHandler import *
from WaterLevelInputDialog import *
from SampleSizeInputDialog import *
from SettingsDialog import *

class TestDialog(QtWidgets.QDialog):
    def __init__(self, socketHandler : SocketHandler, filePath : str, description : str, settings : Settings):
        super().__init__() 

        self.filePath = filePath
        self.description = description
        self.socketHandler = socketHandler
        self.settings = settings

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.formLayout = QtWidgets.QFormLayout() 

        self.sensorSelection = QtWidgets.QComboBox()

        self.sensorSelection.addItem("HC-SR04 Ultrasonic Sensor")
        self.sensorSelection.addItem("Vl5370x Time of Flight Sensor")

        self.formLayout.addRow("Sensor: ",self.sensorSelection)
        self.mainLayout.addLayout(self.formLayout)

        self.accuracyTestButton = QtWidgets.QPushButton("Accuracy Test")
        self.accuracyTestButton.clicked.connect(self.accuracyTest)
        self.mainLayout.addWidget(self.accuracyTestButton)

        self.precisionTestButton = QtWidgets.QPushButton("Precision Test")
        self.precisionTestButton.clicked.connect(self.precisionTest)
        self.mainLayout.addWidget(self.precisionTestButton)

        self.latencyTestButton = QtWidgets.QPushButton("Latency Test") 
        self.latencyTestButton.clicked.connect(self.latencyTest)
        self.mainLayout.addWidget(self.latencyTestButton)

        self.setLayout(self.mainLayout)

        self.socketHandler.done.connect(self.close)

    def getSensorType(self):
        return self.sensorSelection.currentIndex()
    @QtCore.Slot() 
    def accuracyTest(self):
        testParameters = TestParameters()
        testParameters.testType = TestParameters.ACCURACY_TEST
        testParameters.waterLevel = WaterLevelInputDialog().exec()
        testParameters.sampleSize = SampleSizeInputDialog().exec()
        testParameters.sensorType = self.getSensorType()
        SettingsDialog(self.settings, self.socketHandler).exec()

        self.socketHandler.testPrototype.emit(testParameters)

    @QtCore.Slot() 
    def precisionTest(self):
        testParameters = TestParameters()
        testParameters.testType = TestParameters.PRECISION_TEST
        testParameters.sampleSize = SampleSizeInputDialog().exec()
        testParameters.sensorType = self.getSensorType()
        SettingsDialog(self.settings, self.socketHandler).exec()

        self.socketHandler.testPrototype.emit(testParameters)
    @QtCore.Slot()
    def latencyTest(self):
        testParameters = TestParameters()
        testParameters.testType = TestParameters.LATENCY_TEST
        testParameters.sampleSize = SampleSizeInputDialog().exec()
        testParameters.sensorType = self.getSensorType()
        SettingsDialog(self.settings, self  .socketHandler).exec()

        self.socketHandler.testPrototype.emit(testParameters)