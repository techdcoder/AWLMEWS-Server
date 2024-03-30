from StartupWindow import *

def main():
    app = QtWidgets.QApplication()
    app.setApplicationName('AWLMEWS SERVER')
    app.setOrganizationName('The Nocturnals')

    window = StartupWindow()
    window.show()

    app.exec()

    
if __name__ == "__main__":
    main()
