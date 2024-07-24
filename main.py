import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from gui.windows.MainWindow import *
from gui.windows.AboutProgramm import *
from gui.windows.SetWallet import *


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


class AboutProgrammWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(AboutProgrammWindow, self).__init__()
        self.ui = Ui_AboutProgramm()
        self.ui.setupUi(self)


class SetWalletWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(SetWalletWindow, self).__init__()
        self.ui = Ui_SetWallet()
        self.ui.setupUi(self)


def main():       
    app = QtWidgets.QApplication([])
    application = MainWindow()
    application.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
    application.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()