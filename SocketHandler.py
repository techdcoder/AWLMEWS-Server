from PySide6 import QtNetwork
from socket import *
from TestParameters import *
from FileHandler import *

import select


class SocketHandler(QtCore.QObject):
    connected = QtCore.Signal()
    done = QtCore.Signal()
    updated = QtCore.Signal()
    updateTime = QtCore.Signal()

    beginDemoMode = QtCore.Signal()
    demoModeUpdated = QtCore.Signal(float,float)
    endDemoMode = QtCore.Signal()
    demoMode = False

    updateSettings = QtCore.Signal(Settings)
    testPrototype = QtCore.Signal(TestParameters,FileHandler,Settings)

    def __init__(self,port : int):
        super().__init__()

        ipList = QtNetwork.QHostInfo.fromName(QtNetwork.QHostInfo.localHostName()).addresses()

        print("IP Addresses: ")
        for ipAddr in ipList:
            print(ipAddr.toString())

        self.serverSocket = socket(AF_INET,SOCK_STREAM)
        self.location = (ipList[-1].toString(),port)
        self.serverSocket.bind(self.location)
        self.serverSocket.listen()

        self.ipv4,self.port = self.location

        self.updateSettings.connect(self.updateSettingsFunc)
        self.testPrototype.connect(self.testFunc)

        self.beginDemoMode.connect(self.startDemoMode)
        self.endDemoMode.connect(self.terminateDemoMode)

        self.updateTime.connect(self.syncTime)

        self.awlmewsSocket = None
        self.awlmewsAddr = None
    @QtCore.Slot()
    def waitConnection(self):
        self.awlmewsSocket,self.awlmewsAddr = self.serverSocket.accept()
        print("Conneccted to AWLMEWS!")
        self.connected.emit()

    def updateSettingsFunc(self, settings: Settings):
        settings.print()
        msg = settings.encode()
        print(msg)
        self.awlmewsSocket.send(msg.encode())
        self.updated.emit()


    def testFunc(self, testParameters : TestParameters, fileHandler : FileHandler, setting : Settings):
        testParameters.print()
        msg = 't ' + str(testParameters.sampleSize) + ' ' + str(testParameters.sensorType)
        self.awlmewsSocket.send(msg.encode())

        data = []
        mean = 0.0
        deviation = 0.0
        stddev = 0.0
        for i in range(0, testParameters.sampleSize):
            input = self.awlmewsSocket.recv(1024).decode('utf-8')
            waste = self.awlmewsSocket.recv(1024).decode('utf-8')
            value = float(str(input))
            data.append(value)
            mean += value

        self.done.emit()
        mean /= testParameters.sampleSize

        mn, mx = 1000000, 0
        for sample in data:
            deviation += (sample-testParameters.waterLevel)**2
            stddev += (sample-mean)**2
            mn = min(sample,mn)
            mx = max(sample,mx)

        deviation /= testParameters.sampleSize
        stddev /= testParameters.sampleSize

        deviation **= 0.5
        stddev **= 0.5
        r = mx - mn


        if testParameters.testType == testParameters.ACCURACY_TEST:
            fileHandler.writeTestResultAccuracy(setting)
        elif testParameters.testType == testParameters.PRECISION_TEST:
            fileHandler.writeTestResultPrecision(setting)

        print("True Value: ", testParameters.waterLevel)
        print("Mean: ", mean)
        print("STD Dev.", stddev)
        print("Deviation from True Water Level: ", deviation)
        print("Max: ", mx)
        print("Min: ", mn)
        print("Median: ", data[len(data)//2])
        print("Range: ", r)
        print("Difference: ", abs(mean - testParameters.waterLevel))

    @QtCore.Slot()
    def startDemoMode(self):
        msg = "d 1"
        self.awlmewsSocket.sendall(msg.encode())
        self.demoMode = True
        self.demoModeUpdate()

    @QtCore.Slot()
    def terminateDemoMode(self):
        msg = "d 0"
        self.awlmewsSocket.sendall(msg.encode())

    @QtCore.Slot()
    def demoModeUpdate(self):
        while self.demoMode:
            r,_,_ = select.select([self.awlmewsSocket],[],[],0)
            if len(r):
                raw = self.awlmewsSocket.recv(1024)
                msgs = raw.decode('UTF-8')

                msgs = msgs.split('\n')
                for msg in msgs:
                    if len(msg) < 3:
                        continue
                    ultrasonicReading,tofReading = msg.split(' ')
                    self.demoModeUpdated.emit(float(ultrasonicReading),float(tofReading))


    def syncTime(self):
        datetime = QtCore.QDateTime.currentDateTime()
        time = datetime.time()

        msg = "m " + str(time.hour()) + " " + str(time.minute()) + " " +  str(time.second()) + " " + str(time.msec())
        print(msg)
        self.awlmewsSocket.sendall(msg.encode())
    def close(self):
        self.serverSocket.close()