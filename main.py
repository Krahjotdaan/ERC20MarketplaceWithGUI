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
        self.change_price_id = 0
        self.new_price = 0
    
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
                self.incorrect_id()
        except ValueError:
            self.incorrect_id()

        try:
            if int(self.ui.amount_purchase_input.text()) > 0 \
            and int(self.ui.amount_purchase_input.text()) <= self.lots[str(self.purchase_id)][3]:
                self.purchase_amount = int(self.ui.amount_purchase_input.text())
            else:
                self.incorrect_amount()
        except ValueError:
            self.incorrect_amount()

        lot = None
        try:
            lot = self.lots[str(self.purchase_id)]
            self.purchase_cost = self.purchase_amount * lot[2]
            self.ui.purchase_browser.setText(f"""id: {self.purchase_id}\nПродавец: {lot[1]}\nАдрес токена: {lot[0]}\nНазвание: {lot[4]}\nСимвол: {lot[5]}\nДесятичных токенов: {lot[6]}\nЦена за 1 единицу: {lot[2]} wei\nКоличество единиц: {self.purchase_amount}\nИтого: {self.purchase_cost} wei\n\nВставьте в поле ниже приватный ключ. Приватный ключ нужен для подписи отправляемых транзакций. Программа никак не сохраняет его и не передает третьим лицам. Нажмите кнопку "Подтвердить" для отправки транзакции.""")
            self.ui.apply_purchase_button.setEnabled(True)
        except KeyError:
            eras = QtWidgets.QErrorMessage(parent=self)
            eras.showMessage("Такого id нет")
            

    def apply_purchase_button_click(self):
        private_key = self.ui.private_key_input_purchase.text()
        
        try:
            tx_hash = purchase(self.purchase_id, self.purchase_amount, self.purchase_cost, private_key)
            self.tx_browser = TxBrowser(tx_hash)
            self.tx_browser.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
            self.tx_browser.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            self.tx_browser.setFocus()
            self.tx_browser.show()

        except web3.exceptions.Web3ValidationError:
            pass    
        except web3.exceptions.InvalidAddress:
            self.incorrect_wallet()
        except ValueError:
            self.incorrect_private_key()
        except TypeError:
            self.incorrect_private_key()
           
        del(private_key)
        self.purchase_id = 0
        self.purchase_amount = 0
        self.purchase_cost = 0
        self.ui.id_purchase_input.setText("")
        self.ui.amount_purchase_input.setText("")
        self.ui.private_key_input_purchase.setText("")
        self.ui.apply_purchase_button.setEnabled(False)

    def apply_sell_button_click(self):
        token_address = None
        price = 0
        amount = 0
        private_key = None

        try:
            if self.ui.address_sell_input.text()[:2] == "0x":
                token_address = self.ui.address_sell_input.text()
            else:
                self.incorrect_address()
        except:
            self.incorrect_address()

        try:
            if int(self.ui.price_sell_input.text()) > 0:
                price = int(self.ui.price_sell_input.text())
            else:
                self.incorrect_price()
        except ValueError:
            self.incorrect_price()

        try:
            if int(self.ui.amount_sell_input.text()) > 0:
                amount = int(self.ui.amount_sell_input.text())
            else:
                self.incorrect_amount()
        except ValueError:
            self.incorrect_amount()

        private_key = self.ui.private_key_input_sell.text()
        
        try:
            tx_hash = list_lot(token_address, price, amount, private_key)
            self.tx_browser = TxBrowser(tx_hash)
            self.tx_browser.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
            self.tx_browser.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            self.tx_browser.setFocus()
            self.tx_browser.show()

        except web3.exceptions.Web3ValidationError:
            pass
        except web3.exceptions.InvalidAddress:
            self.incorrect_wallet()
        except ValueError:
            self.incorrect_private_key()
        except TypeError:
            self.incorrect_private_key()
           
        del(private_key)
        self.ui.private_key_input_sell.setText("")

    def count_new_price_button_click(self):
        try:
            if int(self.ui.id_change_price_input.text()) > 0:
                self.change_price_id = int(self.ui.id_change_price_input.text())
            else:
                self.incorrect_id()
        except ValueError:
            self.incorrect_id()

        lot = None
        try:
            lot = self.lots[str(self.change_price_id)]
            if int(self.ui.price_change_price_input.text()) > 0 and int(self.ui.price_change_price_input.text()) <= lot[3]:
                self.new_price = int(self.ui.price_change_price_input.text())
                self.ui.change_price_browser.setText(f"""id: {self.change_price_id}\nАдрес токена: {lot[0]}\nНазвание: {lot[4]}\nСимвол: {lot[5]}\nДесятичных токенов: {lot[6]}\nСтарая цена: {lot[2]} wei\nНовая цена: {self.new_price} wei\n\n\n\nВставьте в поле ниже приватный ключ. Приватный ключ нужен для подписи отправляемых транзакций. Программа никак не сохраняет его и не передает третьим лицам. Нажмите кнопку "Подтвердить" для отправки транзакции.""")
                self.ui.apply_change_price_button.setEnabled(True)
            else:
                self.incorrect_price()

        except ValueError:
            self.incorrect_price()
        except KeyError:
            eras = QtWidgets.QErrorMessage(parent=self)
            eras.showMessage("Такого id нет")

    def apply_change_price_button_click(self):
        private_key = self.ui.private_key_input_sell.text()
        
        try:
            tx_hash = change_price(self.change_price_id, self.new_price, private_key)
            self.tx_browser = TxBrowser(tx_hash)
            self.tx_browser.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
            self.tx_browser.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            self.tx_browser.setFocus()
            self.tx_browser.show()

        except web3.exceptions.Web3ValidationError:
            pass
        except web3.exceptions.InvalidAddress:
            self.incorrect_wallet()
        """except ValueError:
            self.incorrect_private_key()
        except TypeError:
            self.incorrect_private_key()"""
           
        del(private_key)
        self.change_price_id = 0
        self.new_price = 0
        self.ui.id_change_price_input.setText("")
        self.ui.price_change_price_input.setText("")
        self.ui.private_key_input_sell.setText("")

    def count_cancel_button_click(self):
        pass

    def apply_cancel_button_click(self):
        pass

    def search_button_click(self):
        pass

    def clear_filter_button_click(self):
        pass

    def incorrect_id(self):
        eras = QtWidgets.QErrorMessage(parent=self)
        eras.showMessage("Некорректный id")
    
    def incorrect_wallet(self):
        eras = QtWidgets.QErrorMessage(parent=self)
        eras.showMessage("Некорректный адрес кошелька")

    def incorrect_private_key(self):
        eras = QtWidgets.QErrorMessage(parent=self)
        eras.showMessage("Некорректный приватный ключ")

    def incorrect_amount(self):
        eras = QtWidgets.QErrorMessage(parent=self)
        eras.showMessage("Некорректное количество")

    def incorrect_price(self):
        eras = QtWidgets.QErrorMessage(parent=self)
        eras.showMessage("Некорректная цена")

    def incorrect_address(self):
        eras = QtWidgets.QErrorMessage(parent=self)
        eras.showMessage("Некорректный адрес")


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
                self.main.incorrect_wallet()
        except:
            self.main.incorrect_wallet()

    def decline(self):
        self.close()


class TxBrowser(QtWidgets.QMainWindow):
    def __init__(self, tx_hash):
        super(TxBrowser, self).__init__()
        self.ui = Ui_TxBrowser()
        self.ui.setupUi(self)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.ui.tx_info.setFont(font)
        self.ui.tx_info.setText(f"Хэш транзакции: {tx_hash}\nПолная информация: https://holesky.etherscan.io/tx/{tx_hash}")


def main():
    app = QtWidgets.QApplication([])
    global APPLICATION
    APPLICATION = MainWindow()
    APPLICATION.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

    APPLICATION.ui.id_purchase_input.setText('1')
    APPLICATION.ui.amount_purchase_input.setText('1000')
    APPLICATION.ui.private_key_input_purchase.setText('0dd85378921b870fa2936eab9d54c6e7b2eb14143a19a0cbcefdf7643cb6ac37')
    set_wallet("0x00adc2ac6677e2E00cCCC232Df3FD01EB1D77673")

    ids = lot_id()
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

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
    thread_list_lot.start()
    thread_cancel.start()
    thread_change_price.start()
    thread_purchase.start()
    