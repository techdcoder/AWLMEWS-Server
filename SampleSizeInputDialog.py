from PySide6 import QtWidgets

class SampleSizeInputDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        self.mainLayout = QtWidgets.QFormLayout()
        self.sampleSizeInput = QtWidgets.QLineEdit()
        self.sampleSizeInput.returnPressed.connect(self.close)

        self.mainLayout.addRow("Sample Size: ", self.sampleSizeInput)

        self.setLayout(self.mainLayout)
    def exec(self):
        super().exec()
        return int(self.sampleSizeInput.text())
