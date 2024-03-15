from PathInputWidget import *

class InfoDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        self.mainLayout = QtWidgets.QFormLayout()

        self.filePathInput = PathInputWidget()
        self.mainLayout.addRow("Path: ",self.filePathInput)

        self.descriptionInput = QtWidgets.QTextEdit()
        self.mainLayout.addRow("Description: ",self.descriptionInput)

        self.buttonRow = QtWidgets.QHBoxLayout()
        self.cancelButton = QtWidgets.QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.cancelCallback)

        self.doneButton = QtWidgets.QPushButton("Done")
        self.doneButton.clicked.connect(self.doneCallback)


        self.buttonRowWidget = QtWidgets.QWidget()

        self.buttonRow.addWidget(self.cancelButton)
        self.buttonRow.addWidget(self.doneButton)
        
        self.buttonRowWidget.setLayout(self.buttonRow)

        self.mainLayout.addWidget(self.buttonRowWidget)

        self.setLayout(self.mainLayout)
    
    def doneCallback(self):
        self.close()

    def cancelCallback(self):
        self.close()

    def exec(self):
        super().exec() 
        return (self.filePathInput.getPath(),self.descriptionInput.toPlainText())