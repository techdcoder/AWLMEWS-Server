from PySide6 import QtWidgets

class WaterLevelInputDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        self.mainLayout = QtWidgets.QFormLayout()
        self.waterLevelInput = QtWidgets.QLineEdit()
        self.mainLayout.addRow("Height (mm): ", self.waterLevelInput)
        self.setLayout(self.mainLayout)
        self.waterLevelInput.returnPressed.connect(self.close)

    def exec(self):
        super().exec()
        waterLevel = float(self.waterLevelInput.text())
        return waterLevel
