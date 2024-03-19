from PySide6 import QtCore
from Settings import *

class FileHandler:
    def __init__(self, path, description):
        self.description = description
        self.file = QtCore.QFile(path)
        self.file.open(QtCore.QIODevice.OpenModeFlag.WriteOnly)

        self.textStream = QtCore.QTextStream(self.file)

    def writeTestResultAccuracy(self, settings : Settings, ):
        self.textStream << "ACCURACY TEST\n"
        self.textStream << "----------------------------------------\n"
        self.textStream << "DESCRIPTION:\n"
        self.textStream << self.description << '\n'
        self.textStream << "----------------------------------------\n"
        settings.writeToFile(self.textStream)
        self.textStream << "----------------------------------------\n"
        pass
    def writeTestResultPrecision(self, settings : Settings):
        self.textStream << "PRECISION TEST"
        self.textStream << "----------------------------------------\n"
        self.textStream << "DESCRIPTION:\n"
        self.textStream << self.description << '\n'
        self.textStream << "----------------------------------------\n"
        settings.writeToFile(self.textStream)
        self.textStream << "----------------------------------------\n"
        pass

    def close(self):
        self.file.close()