from StartupWindow import *

def main():
    app = QtWidgets.QApplication()

    window = StartupWindow()
    window.show()

    app.exec()

    
if __name__ == "__main__":
    main()
