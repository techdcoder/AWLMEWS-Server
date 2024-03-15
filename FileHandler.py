from PySide6 import QtCore

class FileHandler:
    def __init__(self, path):
        self.file = QtCore.QFile(path)
        self.file.open(QtCore.QIODevice.OpenModeFlag.ReadWrite)

    def close(self):
        self.file.close()