from PySide6 import QtCore
class Settings:
    def __init__(self):
        self.ultraSonicSamples = None
        self.tofSamples = None
        self.tofSignalRateLimit = None
        self.tofTimingBudget = None
        self.sirenEnabled = None
        self.iotEnabled = None
        self.facebookEnabled = None
        self.prototypeHeight = None
        self.threshold = None

    def defaultSettings(self):
        self.ultraSonicSamples = 5
        self.tofSamples = 5
        self.tofSignalRateLimit = 0.25
        self.tofTimingBudget = 20000
        self.sirenEnabled = True
        self.iotEnabled = True
        self.facebookEnabled = True
        self.prototypeHeight = 30
        self.threshold = 10.0

    def print(self):
        print("Ultrasonic Samples: ", self.ultraSonicSamples)
        print("TOF Samples", self.tofSamples)
        print("TOF Signal Rate Limit", self.tofSignalRateLimit)
        print("TOF Timing Budget: ", self.tofTimingBudget)
        print("Prototype Height: ", self.prototypeHeight)
        print("IOT Enabled: ", self.iotEnabled)
        print("Facebook Enabled: ", self.facebookEnabled)
        print("Siren Enabled: ", self.sirenEnabled)
        print("Threshold: ", self.threshold)

    def encode(self):
        msg =   ('s ' + str(self.ultraSonicSamples) + ' ' + str(self.tofSamples) + ' '
                + str(self.tofSignalRateLimit) + ' ' + str(self.tofTimingBudget) +
                 ' ' + str(self.prototypeHeight) + ' ' + str(self.threshold) + ' ' + str(int(self.iotEnabled)) + ' '
                 + str(int(self.sirenEnabled)))
        return msg

    def writeToFile(self, file : QtCore.QFile):
        file.write("SETTINGS:\n".encode())
        file.write(f"Ultrasonic Samples: {self.ultraSonicSamples}\n".encode())
        file.write(f"TOF Samples: {self.tofSamples}\n".encode())
        file.write(f"TOF Signal Rate Limit: {self.tofSignalRateLimit}\n".encode())
        file.write(f"TOF Timing Budget: {self.tofTimingBudget}\n".encode())
        file.write(f"Prototype Height: {self.prototypeHeight}\n".encode())
        file.write(f"Threshold: {self.threshold}\n".encode())
        file.write(f"IOT Enabled: {self.iotEnabled}\n".encode())
        file.write(f"Facebook Enabled: {self.facebookEnabled}\n".encode())
        file.write(f"Siren Enabled: {self.sirenEnabled}\n".encode())
