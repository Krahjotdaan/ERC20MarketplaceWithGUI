import sys
from PyQt5 import QtWidgets, QtCore
from application.gui.MainWindow import *
from application.gui.AboutProgramm import *
from application.gui.SetWallet import *
from application.keys import WALLET_ADDRESS, PRINT_EVENT, APPLICATION
from application.event_trackers import thread_list_lot, thread_cancel, thread_change_price, thread_purchase
from application.marketplace_functions import *


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
    
    def about_programm_button_click(self):
        self.about_programm_window = AboutProgrammWindow()
        self.about_programm_window.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.about_programm_window.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.about_programm_window.show()

    def connect_wallet_button_click(self):
        self.set_wallet_window = SetWalletWindow(self)
        self.set_wallet_window.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.set_wallet_window.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.set_wallet_window.show()

    def count_cost_button_click(self):
        pass

    def apply_purchase_button_click(self):
        pass

    def apply_sell_button_click(self):
        pass

    def count_new_price_button_click(self):
        pass

    def apply_change_price_button_click(self):
        pass

    def count_cancel_button_click(self):
        pass

    def apply_cancel_button_click(self):
        pass

    def search_button_click(self):
        pass

    def clear_filter_button_click(self):
        pass


class AboutProgrammWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(AboutProgrammWindow, self).__init__()
        self.ui = Ui_AboutProgramm()
        self.ui.setupUi(self)


class SetWalletWindow(QtWidgets.QDialog):
    def __init__(self, root):
        super(SetWalletWindow, self).__init__()
        self.ui = Ui_SetWallet()
        self.ui.setupUi(self)
        self.main = root

    def accept(self):
        try:
            if self.ui.wallet_input.text()[:2] == "0x":
                global WALLET_ADDRESS
                WALLET_ADDRESS = self.ui.wallet_input.text()
                self.main.ui.wallet_label.setText(f"Кошелек: {WALLET_ADDRESS}")
                self.close()
            else:
                eras = QtWidgets.QErrorMessage(parent=self)
                eras.showMessage("Некорректный адрес")
        except:
            eras = QtWidgets.QErrorMessage(parent=self)
            eras.showMessage("Некорректный адрес")

    def decline(self):
        self.close()

def main():
    app = QtWidgets.QApplication([])
    global APPLICATION
    APPLICATION = MainWindow()
    APPLICATION.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
    APPLICATION.show()

    """thread_list_lot.start()
    thread_cancel.start()
    thread_change_price.start()
    thread_purchase.start()"""

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
    