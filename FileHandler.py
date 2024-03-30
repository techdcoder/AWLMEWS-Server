from PySide6 import QtCore
from Settings import *

class FileHandler:
    def __init__(self, path, description):
        self.description = description
        self.file = QtCore.QFile(path)
        self.file.open(QtCore.QIODevice.OpenModeFlag.WriteOnly)

        self.textStream = QtCore.QTextStream(self.file)

    def writeTestResultAccuracy(self, settings : Settings, ):
        self.file.write("ACCURACY TEST\n".encode())
        self.file.write("----------------------------------------\n".encode())
        self.file.write(f"Description:\n{self.description}\n".encode())
        self.file.write("----------------------------------------\n".encode())
        settings.writeToFile(self.file)
        self.file.write("----------------------------------------\n".encode())

    def writeTestResultPrecision(self, settings : Settings):
        self.file.write("PRECISION TEST\n".encode())
        self.file.write("----------------------------------------\n".encode())
        self.file.write(f"Description:\n{self.description}\n".encode())
        self.file.write("----------------------------------------\n".encode())
        settings.writeToFile(self.file)
        self.file.write("----------------------------------------\n".encode())

    def writeStr(self,str):
        self.file.write(str.encode())

    def close(self):
        self.file.close()