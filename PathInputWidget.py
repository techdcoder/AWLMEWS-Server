from PySide6 import QtWidgets, QtCore 

class PathInputWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.mainLayout = QtWidgets.QHBoxLayout()

        self.pathInput = QtWidgets.QLineEdit()
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
        return self.pathInput.text()