from PySide6 import QtCore
from socket import *
from Settings import *
from TestParameters import *


class SocketHandler(QtCore.QObject):
    connected = QtCore.Signal()
    done = QtCore.Signal()
    updated = QtCore.Signal()

    updateSettings = QtCore.Signal(Settings)
    testPrototype = QtCore.Signal(TestParameters)

    def __init__(self,port : int):
        super().__init__()

        self.serverSocket = socket(AF_INET,SOCK_STREAM)
        self.location = ("192.168.1.39",port)
        self.serverSocket.bind(self.location)
        self.serverSocket.listen()

        self.ipv4,self.port = self.location

        self.updateSettings.connect(self.updateSettingsFunc)
        self.testPrototype.connect(self.testFunc)

        self.awlmewsSocket = None
        self.awlmewsAddr = None
    @QtCore.Slot()
    def waitConnection(self):
        self.awlmewsSocket,self.awlmewsAddr = self.serverSocket.accept()
        print("Conneccted to AWLMEWS!")
        self.connected.emit()

    def updateSettingsFunc(self, settings: Settings):
        settings.print()
        msg = 's ' + str(settings.ultraSonicSamples) + ' ' + str(settings.tofSamples) + ' ' + str(settings.tofSignalRateLimit) + ' ' + str(settings.tofTimingBudget)
        print(msg)
        self.awlmewsSocket.send(msg.encode())
        self.updated.emit()


    def testFunc(self, testParameters : TestParameters):
        testParameters.print()
        msg = 't ' + str(testParameters.sampleSize) + ' ' + str(testParameters.sensorType)
        print(msg)
        self.awlmewsSocket.send(msg.encode())

        data = []
        mean = 0.0
        deviation = 0.0
        stddev = 0.0
        for i in range(0, testParameters.sampleSize):
            print("HELLO")
            input = self.awlmewsSocket.recv(1024).decode('utf-8')
            waste = self.awlmewsSocket.recv(1024).decode('utf-8')
            value = float(str(input))
            data.append(value)
            mean += value
            print(value)

        self.done.emit()
        mean /= testParameters.sampleSize

        for sample in data:
            deviation += (sample-testParameters.waterLevel)**2
            stddev += (sample-mean)**2
        deviation /= testParameters.sampleSize
        stddev /= testParameters.sampleSize

        deviation **= 0.5
        stddev **= 0.5

        print("True Value: ", testParameters.waterLevel)
        print("Mean: ", mean)
        print("STD Dev.", stddev)
        print("Deviation from True Water Level: ", deviation)

    def close(self):
        self.serverSocket.close()
