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
        msg = settings.encode() + "\n"
        print(msg)
        self.awlmewsSocket.send(msg.encode())
        self.updated.emit()



    def testFunc(self, testParameters : TestParameters, fileHandler : FileHandler, setting : Settings):
        testParameters.print()
        if testParameters.testType == testParameters.LATENCY_TEST:
            fileHandler.writeStr(f"Sample Size: {testParameters.sampleSize}\n")
            fileHandler.writeStr("SENSOR TYPE: ")
            if testParameters.sensorType == testParameters.ULTRASONIC_SENSOR:
                fileHandler.writeStr("ULTRASONIC\n")
            else:
                fileHandler.writeStr("TOF\n")
            fileHandler.writeStr("Latencies:\n")


            print("LATENCY TEST")



            self.syncTime()
            msg = 'l ' + str(testParameters.sampleSize) + ' ' + str(testParameters.sensorType)
            self.awlmewsSocket.sendall(msg.encode())

            latencyAvg = 0
            for i in range(0,testParameters.sampleSize):
                startTime = QtCore.QDateTime.currentDateTime().time()
                while True:
                    buf = self.awlmewsSocket.recv(1024)
                    if len(buf) >= 2:
                        break
                endTime = QtCore.QDateTime.currentDateTime().time()
                if i < testParameters.sampleSize:
                    self.awlmewsSocket.sendall("ping\n".encode())

                diff = (endTime.hour()-startTime.hour())*60*60*1000 + (endTime.minute()-startTime.minute())*60*1000 + (endTime.second()-startTime.second())*1000 + (endTime.msec() - startTime.msec())
                latencyAvg += diff
                print("DIFF: ", diff)
                fileHandler.writeStr(f"{diff}ms\n")
            fileHandler.writeStr(f"Average Latency: {latencyAvg / testParameters.sampleSize}ms\n")
            print("AVERAGE LATENCY: ", latencyAvg / testParameters.sampleSize)
            fileHandler.file.close()
            return
        msg = 't ' + str(testParameters.sampleSize) + ' ' + str(testParameters.sensorType) + '\n'
        self.awlmewsSocket.send(msg.encode())
        data = []
        mean = 0.0
        deviation = 0.0
        stddev = 0.0

        count = 0
        while True:
            input = self.awlmewsSocket.recv(1024).decode('utf-8')
            processed = ""
            done = False
            for ch in input:
                processed += ch
                if ch == '\n' or ch == '\r':
                    if len(processed) < 3:
                        break
                    processed = processed[:-1]
                    count += 1
                    value = float(str(processed))
                    print("COUNT: ", count, " VALUE: ",value)
                    data.append(value)
                    mean += value
                    if count == testParameters.sampleSize:
                        done = True
                        break
            if done:
                break
        mean /= testParameters.sampleSize

        mn, mx = 1000000, 0
        errors = []
        errorAvg = 0
        for sample in data:
            deviation += (sample-testParameters.waterLevel)**2
            stddev += (sample-mean)**2
            mn = min(sample,mn)
            mx = max(sample,mx)
            error = abs(sample - testParameters.waterLevel) / testParameters.waterLevel * 100
            errorAvg += error
            errors.append(error)
        errorAvg /= testParameters.sampleSize
        deviation /= testParameters.sampleSize
        stddev /= testParameters.sampleSize

        deviation **= 0.5
        stddev **= 0.5
        r = mx - mn


        if testParameters.testType == testParameters.ACCURACY_TEST:
            fileHandler.writeTestResultAccuracy(setting)
        elif testParameters.testType == testParameters.PRECISION_TEST:
            fileHandler.writeTestResultPrecision(setting)

        fileHandler.writeStr(f"Sample Size: {testParameters.sampleSize}\n")
        fileHandler.writeStr(f"Sensor Type: ")
        if testParameters.sensorType == testParameters.ULTRASONIC_SENSOR:
            fileHandler.writeStr("ULTRASONIC\n")
        else:
            fileHandler.writeStr("TOF\n")

        fileHandler.writeStr(f"True Value: {testParameters.waterLevel}\n")
        fileHandler.writeStr(f"Mean: {mean}\n")
        fileHandler.writeStr(f"STD Dev.: {stddev}\n")
        fileHandler.writeStr(f"Deviation from Water Level: {deviation}\n")
        fileHandler.writeStr(f"Max: {mx}\n")
        fileHandler.writeStr(f"Min: {mn}\n")
        fileHandler.writeStr(f"Median: {data[len(data)//2]}\n")
        fileHandler.writeStr(f"Range: {r}\n")
        fileHandler.writeStr(f"Difference: {abs(mean - testParameters.waterLevel)}\n")
        fileHandler.writeStr(f"Average Error {errorAvg}%\n")
        print("True Value: ", testParameters.waterLevel)
        print("Mean: ", mean)
        print("STD Dev.", stddev)
        print("Deviation from True Water Level: ", deviation)
        print("Max: ", mx)
        print("Min: ", mn)
        print("Median: ", data[len(data)//2])
        print("Range: ", r)
        print("Difference: ", abs(mean - testParameters.waterLevel))
        print("Average Error: ", errorAvg, "%")

        fileHandler.writeStr("\nDATA:\n----------------------------------------\n")


        for sample in data:
            fileHandler.writeStr(f"{sample}\n")

        fileHandler.writeStr("\nERROR   :\n----------------------------------------\n")
        for error in errors:
            fileHandler.writeStr(f"{error}%\n")
        fileHandler.file.close()
        self.done.emit()

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
        print("SYNC TIME DOES NOTHING")
        pass
    def close(self):
        self.serverSocket.close()