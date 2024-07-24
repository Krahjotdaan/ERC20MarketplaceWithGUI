import sys
from PyQt5 import QtWidgets, QtCore
from application.gui.MainWindow import *
from application.gui.AboutProgramm import *
from application.gui.SetWallet import *
from application.keys import WALLET_ADDRESS, PRINT_EVENT
from application.event_trackers import thread_list_lot, thread_cancel, thread_change_price, thread_purchase


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
    
    def about_programm_button_click(self):
        self.about_programm_window = AboutProgrammWindow()
        self.about_programm_window.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.about_programm_window.show()

    def connect_wallet_button_click(self):
        self.set_wallet_window = SetWalletWindow()
        self.set_wallet_window.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.set_wallet_window.show()


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
    thread_list_lot.start()
    thread_cancel.start()
    thread_change_price.start()
    thread_purchase.start()
