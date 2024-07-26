import sys, web3
from PyQt5 import QtWidgets, QtCore
from application.gui.MainWindow import *
from application.gui.AboutProgramm import *
from application.gui.SetWallet import *
from application.gui.TxBrowser import *
from application.keys import APPLICATION, set_wallet
from application.event_trackers import thread_list_lot, thread_cancel, thread_change_price, thread_purchase
from application.marketplace_functions import *


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.lots = {}
        self.lot_widgets = []
        self.purchase_id = 0
        self.purchase_amount = 0
        self.purchase_cost = 0
    
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
        try:
            if int(self.ui.id_purchase_input.text()) > 0:
                self.purchase_id = int(self.ui.id_purchase_input.text())

            else:
                eras = QtWidgets.QErrorMessage(parent=self)
                eras.showMessage("id должен быть больше 0")
        except ValueError:
            eras = QtWidgets.QErrorMessage(parent=self)
            eras.showMessage("Некорректный id")

        try:
            if int(self.ui.amount_purchase_input.text()) > 0:
                self.purchase_amount = int(self.ui.amount_purchase_input.text())
            else:
                eras = QtWidgets.QErrorMessage(parent=self)
                eras.showMessage("Количество должно быть больше 0")
        except ValueError:
            eras = QtWidgets.QErrorMessage(parent=self)
            eras.showMessage("Некорректное количество")

        lot = self.lots[str(self.purchase_id)]
        self.purchase_cost = self.purchase_amount * lot[2]
        self.ui.purchase_browser.setText(f"""id: {self.purchase_id}\nПродавец: {lot[0]}\nАдрес токена: {lot[1]}\nНазвание: {lot[4]}\nСимвол: {lot[5]}\nДесятичных токенов: {lot[6]}\nЦена за 1 единицу: {lot[2]} wei\nКоличество единиц: {self.purchase_amount}\nИтого: {self.purchase_cost} wei\n\nВставьте в поле ниже приватный ключ. Приватный ключ нужен для подписи отправляемых транзакций. Программа никак не сохраняет его и не передает третьим лицам. Нажмите кнопку "Подтвердить" для отправки транзакции.""")
        self.ui.apply_purchase_button.setEnabled(True)
            

    def apply_purchase_button_click(self):
        pass

    def apply_sell_button_click(self):
        token_address = None
        price = 0
        amount = 0
        private_key = None

        try:
            if self.ui.address_sell_input.text()[:2] == "0x":
                token_address = self.ui.address_sell_input.text()
            else:
                eras = QtWidgets.QErrorMessage(parent=self)
                eras.showMessage("Некорректный адрес")
        except:
            eras = QtWidgets.QErrorMessage(parent=self)
            eras.showMessage("Некорректный адрес")

        try:
            if int(self.ui.price_sell_input.text()) > 0:
                price = int(self.ui.price_sell_input.text())
            else:
                eras = QtWidgets.QErrorMessage(parent=self)
                eras.showMessage("Цена должна быть больше 0")
        except ValueError:
            eras = QtWidgets.QErrorMessage(parent=self)
            eras.showMessage("Некорректная цена")

        try:
            if int(self.ui.amount_sell_input.text()) > 0:
                amount = int(self.ui.amount_sell_input.text())
            else:
                eras = QtWidgets.QErrorMessage(parent=self)
                eras.showMessage("Количество должно быть больше 0")
        except ValueError:
            eras = QtWidgets.QErrorMessage(parent=self)
            eras.showMessage("Некорректное количество")

        private_key = self.ui.private_key_input_sell.text()
        
        try:
            tx_hash = list_lot(token_address, price, amount, private_key)
            self.tx_browser = TxBrowser(tx_hash)
            self.tx_browser.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
            self.tx_browser.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            self.tx_browser.show()

        except web3.exceptions.Web3ValidationError:
            pass
        
        except web3.exceptions.InvalidAddress:
            eras = QtWidgets.QErrorMessage(parent=self)
            eras.showMessage("Некорректный адрес кошелька")
           
        del(private_key)
        self.ui.private_key_input_sell.setText("")

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
                set_wallet(self.ui.wallet_input.text())
                self.main.ui.wallet_label.setText(f"Кошелек: {self.ui.wallet_input.text()}")
                self.close()
            else:
                eras = QtWidgets.QErrorMessage(parent=self)
                eras.showMessage("Некорректный адрес")
        except:
            eras = QtWidgets.QErrorMessage(parent=self)
            eras.showMessage("Некорректный адрес")

    def decline(self):
        self.close()


class TxBrowser(QtWidgets.QMainWindow):
    def __init__(self, tx_hash):
        super(TxBrowser, self).__init__()
        self.ui = Ui_TxBrowser()
        self.ui.setupUi(self)
        self.ui.tx_info.setText(f"Хэш транзакции: {tx_hash}\n \
                                Полная информация: https://holesky.etherscan.io/tx/{tx_hash}")


def main():
    app = QtWidgets.QApplication([])
    global APPLICATION
    APPLICATION = MainWindow()
    APPLICATION.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

    ids = lot_id()
    global lots
    for i in range(1, ids + 1):
        lot = lot_info(i)
        if lot[3] > 0:
            APPLICATION.lots[str(i)] = lot
            lot_widget = QtWidgets.QListWidgetItem()
            font = QtGui.QFont()
            font.setPointSize(12)
            lot_widget.setFont(font)
            lot_widget.setText(f"id: {i}\nПродавец: {lot[1]}\nАдрес токена: {lot[0]}\nНазвание: {lot[4]}\nСимвол: {lot[5]}\nДесятичных токенов: {lot[6]}\nЦена за 1 единицу: {lot[2]} wei\nКоличество единиц: {lot[3]}\n")
            APPLICATION.lot_widgets.append(lot_widget)

    for item in APPLICATION.lot_widgets:
        APPLICATION.ui.list_all_lots.addItem(item)
    APPLICATION.show()

    """thread_list_lot.start()
    thread_cancel.start()
    thread_change_price.start()
    thread_purchase.start()"""

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
    