from PySide6 import QtWidgets, QtCore 

class PathInputWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.testPathSetting = QtCore.QSettings()

        self.mainLayout = QtWidgets.QHBoxLayout()

        self.path = self.testPathSetting.value("SavePath")
        if self.path == None:
            self.pathInput = QtWidgets.QLineEdit()
        else:
            self.pathInput = QtWidgets.QLineEdit(self.path)

        self.openButton = QtWidgets.QPushButton("Open")
        self.openButton.clicked.connect(self.openButtonCallback)

        self.mainLayout.addWidget(self.pathInput)
        self.mainLayout.addWidget(self.openButton)

        self.setLayout(self.mainLayout)

    @QtCore.Slot()
    def openButtonCallback(self):
        dialog = QtWidgets.QFileDialog()
        path,filetype = dialog.getSaveFileName()

        self.pathInput.setText(path)
    
    def getPath(self):
        path = self.pathInput.text()
        self.testPathSetting.setValue('SavePath',path)
        return path