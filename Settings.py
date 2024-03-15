class Settings:
    def __init__(self):
        self.ultraSonicSamples = None
        self.tofSamples = None
        self.tofSignalRateLimit = None
        self.tofTimingBudget = None

    def defaultSettings(self):
        self.ultraSonicSamples = 5
        self.tofSamples = 5
        self.tofSignalRateLimit = 0.25
        self.tofTimingBudget = 20000

    def print(self):
        print("Ultrasonic Samples: ", self.ultraSonicSamples)
        print("TOF Samples", self.tofSamples)
        print("TOF Signal Rate Limit", self.tofSignalRateLimit)
        print("TOF Timing Budget: ", self.tofTimingBudget)