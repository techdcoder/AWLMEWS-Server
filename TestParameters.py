class TestParameters:
    ACCURACY_TEST = 0
    PRECISION_TEST = 1
    LATENCY_TEST = 2

    ULTRASONIC_SENSOR = 0
    TOF_SENSOR = 1

    def __init__(self):
        self.sampleSize = None
        self.testType = None
        self.waterLevel = None
        self.sensorType = None
    def print(self):
        tmapping = {0:"ACCURACY TEST",1:"PRECISION TEST",2:"LATENCY TEST"}
        smapping = {0:"ULTRASONIC SENSOR",1:"TOF SENSOR"}

        print("Sample Size: ", self.sampleSize)
        print("Test Type: ", tmapping[self.testType])
        print("Sensor Type: ", smapping[self.sensorType])