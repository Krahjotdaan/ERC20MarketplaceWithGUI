import os, sys, web3
from PyQt5 import QtWidgets, QtCore
from application.gui.MainWindow import *
from application.gui.AboutProgramm import *
from application.gui.SetWallet import *
from application.gui.TxBrowser import *
from application.gui.SearchWindow import *
from application.gui.SearchResults import *
from application.gui.error_messages import *
from application.keys import set_application, set_wallet, get_wallet
from application.event_trackers import thread_list_lot, thread_cancel, thread_change_price, thread_purchase
from application.marketplace_functions import *


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.lots = {}
        self.lot_widgets = {}
        self.my_lots_widgets = {}
        self.purchase_id = 0
        self.purchase_amount = 0
        self.purchase_cost = 0
        self.change_price_id = 0
        self.new_price = 0
        self.cancel_id = 0
        self.cancel_amount = 0
        self.remain_amount = 0
    
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

    def search_button_click(self):
        self.search_window = SearchWindow(self)
        self.search_window.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.search_window.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.search_window.show()

    def count_cost_button_click(self):
        try:
            if int(self.ui.id_purchase_input.text()) > 0:
                self.purchase_id = int(self.ui.id_purchase_input.text())
            else:
                incorrect_id(self)
        except ValueError:
            incorrect_id(self)

        lot = None
        try:
            lot = self.lots[str(self.purchase_id)]
            if int(self.ui.amount_purchase_input.text()) > 0 and int(self.ui.amount_purchase_input.text()) <= lot[3]:
                self.purchase_amount = int(self.ui.amount_purchase_input.text())
                self.purchase_cost = self.purchase_amount * lot[2]
                self.ui.purchase_browser.setText(f"""id: {self.purchase_id}\nПродавец: {lot[0]}\nАдрес токена: {lot[1]}\nНазвание: {lot[4]}\nСимвол: {lot[5]}\nДесятичных токенов: {lot[6]}\nЦена за 1 единицу: {lot[2]} wei\nКоличество единиц: {self.purchase_amount}\nИтого: {self.purchase_cost} wei\n\nВставьте в поле ниже приватный ключ. Приватный ключ нужен для подписи отправляемых транзакций. Программа никак не сохраняет его и не передает третьим лицам. Нажмите кнопку "Подтвердить" для отправки транзакции.""")
                self.ui.apply_purchase_button.setEnabled(True)
                self.ui.private_key_input_purchase.setEnabled(True)
            else:
                incorrect_amount(self)
        except ValueError:
            incorrect_amount(self)       
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
            incorrect_wallet(self)
        except TypeError:
            incorrect_private_key(self)    
        except ValueError:
            eras = QtWidgets.QErrorMessage(parent=self)
            eras.showMessage("Ошибка сети. Транзакция не отправлена")
        
        del private_key
        self.purchase_id = 0
        self.purchase_amount = 0
        self.purchase_cost = 0
        self.ui.id_purchase_input.setText("")
        self.ui.amount_purchase_input.setText("")
        self.ui.private_key_input_purchase.setText("")
        self.ui.apply_purchase_button.setEnabled(False)
        self.ui.private_key_input_purchase.setEnabled(False)
        self.ui.purchase_browser.setText("""id:\nПродавец:\nАдрес токена:\nНазвание:\nСимвол:\nДесятичных токенов:\nЦена за 1 единицу:\nКоличество единиц:\nИтого:\n\nВставьте в поле ниже приватный ключ. Приватный ключ нужен для подписи отправляемых транзакций. Программа никак не сохраняет его и не передает третьим лицам. Нажмите кнопку "Подтвердить" для отправки транзакции.""")

    def apply_sell_button_click(self):
        token_address = None
        price = 0
        amount = 0
        private_key = None

        try:
            if self.ui.address_sell_input.text()[:2] == "0x":
                token_address = self.ui.address_sell_input.text()
            else:
                incorrect_address(self)
        except:
            incorrect_address(self)

        try:
            if int(self.ui.price_sell_input.text()) > 0:
                price = int(self.ui.price_sell_input.text())
            else:
                incorrect_price(self)
        except ValueError:
            incorrect_price(self)

        try:
            if int(self.ui.amount_sell_input.text()) > 0:
                amount = int(self.ui.amount_sell_input.text())
            else:
                incorrect_amount(self)
        except ValueError:
            incorrect_amount(self)

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
            incorrect_wallet(self)
        except ValueError:
            incorrect_private_key(self)
        except TypeError:
            incorrect_private_key(self)
           
        del(private_key)
        self.ui.address_sell_input.setText("")
        self.ui.price_sell_input.setText("")
        self.ui.amount_sell_input.setText("")
        self.ui.private_key_input_sell.setText("")

    def count_new_price_button_click(self):
        try:
            if int(self.ui.id_change_price_input.text()) > 0:
                self.change_price_id = int(self.ui.id_change_price_input.text())
            else:
                incorrect_id(self)
        except ValueError:
            incorrect_id(self)

        lot = None
        try:
            lot = self.lots[str(self.change_price_id)]
            if int(self.ui.price_change_price_input.text()) > 0 and int(self.ui.price_change_price_input.text()) != lot[3]:
                self.new_price = int(self.ui.price_change_price_input.text())
                self.ui.change_price_browser.setText(f"""id: {self.change_price_id}\nАдрес токена: {lot[1]}\nНазвание: {lot[4]}\nСимвол: {lot[5]}\nДесятичных токенов: {lot[6]}\nСтарая цена: {lot[2]} wei\nНовая цена: {self.new_price} wei\n\n\n\nВставьте в поле ниже приватный ключ. Приватный ключ нужен для подписи отправляемых транзакций. Программа никак не сохраняет его и не передает третьим лицам. Нажмите кнопку "Подтвердить" для отправки транзакции.""")
                self.ui.apply_change_price_button.setEnabled(True)
                self.ui.private_key_input_change_price.setEnabled(True)
            else:
                incorrect_price(self)

        except ValueError:
            incorrect_price(self)
        except KeyError:
            eras = QtWidgets.QErrorMessage(parent=self)
            eras.showMessage("Такого id нет")

    def apply_change_price_button_click(self):
        private_key = self.ui.private_key_input_change_price.text()
        
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
            incorrect_wallet(self)
        except ValueError:
            incorrect_private_key(self)
        except TypeError:
            incorrect_private_key(self)
           
        del private_key
        self.change_price_id = 0
        self.new_price = 0
        self.ui.id_change_price_input.setText("")
        self.ui.price_change_price_input.setText("")
        self.ui.private_key_input_change_price.setText("")
        self.ui.apply_change_price_button.setEnabled(False)
        self.ui.private_key_input_change_price.setEnabled(False)
        self.ui.change_price_browser.setText(f"""id:\nАдрес токена:\nНазвание:\nСимвол:\nДесятичных токенов:\nСтарая цена:\nНовая цена:\n\n\n\nВставьте в поле ниже приватный ключ. Приватный ключ нужен для подписи отправляемых транзакций. Программа никак не сохраняет его и не передает третьим лицам. Нажмите кнопку "Подтвердить" для отправки транзакции.""")

    def count_cancel_button_click(self):
        try:
            if int(self.ui.id_cancel_input.text()) > 0:
                self.cancel_id = int(self.ui.id_cancel_input.text())
            else:
                incorrect_id(self)
        except ValueError:
            incorrect_id(self)

        lot = None
        try:
            lot = self.lots[str(self.cancel_id)]
            if int(self.ui.amount_cancel_input.text()) > 0 and int(self.ui.amount_cancel_input.text()) <= lot[3]:
                self.cancel_amount = int(self.ui.amount_cancel_input.text())
                self.ui.cancel_browser.setText(f"""id: {self.cancel_id}\nАдрес токена: {lot[1]}\nНазвание: {lot[4]}\nСимвол: {lot[5]}\nДесятичных токенов: {lot[6]}\nЦена за 1 единицу: {lot[2]} wei\nБудет снято с продажи(ед. токенов): {self.cancel_amount}\nОстанется в продаже: {lot[3] - self.cancel_amount}\n\n\nВставьте в поле ниже приватный ключ. Приватный ключ нужен для подписи отправляемых транзакций. Программа никак не сохраняет его и не передает третьим лицам. Нажмите кнопку "Подтвердить" для отправки транзакции.""")
                self.ui.apply_cancel_button.setEnabled(True)
                self.ui.private_key_input_cancel.setEnabled(True)
            else:
                incorrect_amount(self)
        except ValueError:
            incorrect_amount(self)
        except KeyError:
            eras = QtWidgets.QErrorMessage(parent=self)
            eras.showMessage("Такого id нет")

    def apply_cancel_button_click(self):
        private_key = self.ui.private_key_input_cancel.text()
        
        try:
            tx_hash = cancel(self.cancel_id, self.cancel_amount, private_key)
            self.tx_browser = TxBrowser(tx_hash)
            self.tx_browser.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
            self.tx_browser.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            self.tx_browser.setFocus()
            self.tx_browser.show()

        except web3.exceptions.Web3ValidationError:
            pass
        except web3.exceptions.InvalidAddress:
            incorrect_wallet(self)
        except ValueError:
            incorrect_private_key(self)
        except TypeError:
            incorrect_private_key(self)
           
        del private_key
        self.cancel_id = 0
        self.cancel_amount = 0
        self.ui.id_cancel_input.setText("")
        self.ui.amount_cancel_input.setText("")
        self.ui.private_key_input_cancel.setText("")
        self.ui.apply_cancel_button.setEnabled(False)
        self.ui.private_key_input_cancel.setEnabled(False)
        self.ui.cancel_browser.setText(f"""id:\nАдрес токена:\nНазвание:\nСимвол:\nДесятичных токенов:\nЦена за 1 единицу:wei\nБудет снято с продажи(ед. токенов):\nОстанется в продаже:\n\n\nВставьте в поле ниже приватный ключ. Приватный ключ нужен для подписи отправляемых транзакций. Программа никак не сохраняет его и не передает третьим лицам. Нажмите кнопку "Подтвердить" для отправки транзакции.""")

    def logs_journal_button_click(self):
        os.startfile("logs.log")
    
    def create_lot_widget(self, id, lot):
        lot_widget = QtWidgets.QListWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(12)
        lot_widget.setFont(font)
        lot_widget.setText(f"id: {id}\nПродавец: {lot[0]}\nАдрес токена: {lot[1]}\nНазвание: {lot[4]}\nСимвол: {lot[5]}\nДесятичных токенов: {lot[6]}\nЦена за 1 единицу: {lot[2]} wei\nКоличество единиц: {lot[3]}\n")
        self.lot_widgets[str(id)] = lot_widget
        self.ui.list_all_lots.addItem(lot_widget)
        if lot[0] == get_wallet():
            my_lot_widget = QtWidgets.QListWidgetItem()
            my_lot_widget.setFont(font)
            my_lot_widget.setText(f"id: {id}\nПродавец: {lot[0]}\nАдрес токена: {lot[1]}\nНазвание: {lot[4]}\nСимвол: {lot[5]}\nДесятичных токенов: {lot[6]}\nЦена за 1 единицу: {lot[2]} wei\nКоличество единиц: {lot[3]}\n")
            self.my_lots_widgets[str(id)] = my_lot_widget
            self.ui.list_my_lots.addItem(my_lot_widget)


class AboutProgrammWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(AboutProgrammWindow, self).__init__()
        self.ui = Ui_AboutProgramm()
        self.ui.setupUi(self)


class SetWalletWindow(QtWidgets.QDialog):
    def __init__(self, root : MainWindow):
        super(SetWalletWindow, self).__init__()
        self.ui = Ui_SetWallet()
        self.ui.setupUi(self)
        self.main = root

    def accept(self):
        try:
            if self.ui.wallet_input.text()[:2] == "0x":
                set_wallet(self.ui.wallet_input.text())
                self.main.ui.wallet_label.setText(f"Кошелек: {self.ui.wallet_input.text()}")

                with open('wallet.txt', 'w') as fl:
                    fl.write(self.ui.wallet_input.text())

                self.main.ui.list_my_lots.clear()
                self.main.my_lots_widgets.clear()
                for id in self.main.lots.keys():
                    if self.main.lots[id][0] == get_wallet():
                        lot = self.main.lots[id]
                        my_lot_widget = QtWidgets.QListWidgetItem()
                        font = QtGui.QFont()
                        font.setPointSize(12)
                        my_lot_widget.setFont(font)
                        my_lot_widget.setText(f"id: {id}\nПродавец: {lot[0]}\nАдрес токена: {lot[1]}\nНазвание: {lot[4]}\nСимвол: {lot[5]}\nДесятичных токенов: {lot[6]}\nЦена за 1 единицу: {lot[2]} wei\nКоличество единиц: {lot[3]}\n")
                        self.main.my_lots_widgets[str(id)] = my_lot_widget
                        self.main.ui.list_my_lots.addItem(my_lot_widget)

                self.close()
            else:
                incorrect_wallet(self)
        except:
            incorrect_wallet(self)

    def decline(self):
        self.close()


class TxBrowser(QtWidgets.QMainWindow):
    def __init__(self, tx_hash):
        super(TxBrowser, self).__init__()
        self.ui = Ui_TxBrowser()
        self.ui.setupUi(self)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.ui.tx_info.setFont(font)
        self.ui.tx_info.setText(f"Хэш транзакции: {tx_hash}\nПолная информация: https://holesky.etherscan.io/tx/{tx_hash}")


class SearchWindow(QtWidgets.QMainWindow):
    def __init__(self, root : MainWindow):
        super(SearchWindow, self).__init__()
        self.ui = Ui_SearchWindow()
        self.ui.setupUi(self)
        self.main = root

    def by_id_button_click(self):
        results = {}
        try:
            if int(self.ui.by_id_input.text()) > 0:
                id = int(self.ui.by_id_input.text())
                lot = self.main.lots[str(id)]
                results[str(id)] = lot
                self.show_results(id, results)
            else:
                incorrect_id(self)
        except ValueError:
            incorrect_id(self)
        except KeyError:
            eras = QtWidgets.QErrorMessage(parent=self)
            eras.showMessage("Такого id нет")

    def by_address_button_click(self):
        results = {}
        address = ""
        try:
            if self.ui.by_address_input.text()[:2] == "0x":
                address = self.ui.by_address_input.text()
                for key in self.main.lots.keys():
                    if self.main.lots[key][1] == address:
                        results[key] = self.main.lots[key]
            else:
                incorrect_address(self)
        except:
            incorrect_address(self)
        
        if len(results.keys()) == 0:
            eras = QtWidgets.QErrorMessage(parent=self)
            eras.showMessage("Ничего не найдено")
        else:
            self.show_results(address, results)

    def by_name_button_click(self):
        results = {}
        name = ""
        try:
            name = self.ui.by_name_input.text()
            for key in self.main.lots.keys():
                if self.main.lots[key][4] == name:
                    results[key] = self.main.lots[key]
        except:
            eras = QtWidgets.QErrorMessage(parent=self)
            eras.showMessage("Некорректное название")
        
        if len(results.keys()) == 0:
            eras = QtWidgets.QErrorMessage(parent=self)
            eras.showMessage("Ничего не найдено")
        else:
            self.show_results(name, results)

    def show_results(self, template, results):
        self.search_results_window = SearchResultsWindow(template, results)
        self.search_results_window.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.search_results_window.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.search_results_window.show()


class SearchResultsWindow(QtWidgets.QMainWindow):
    def __init__(self, template, results : dict):
        super(SearchResultsWindow, self).__init__()
        self.ui = Ui_SearchResults()
        self.ui.setupUi(self)
        self.results = results
        self.ui.label.setText(f"""Результаты поиска по "{str(template)}" """)

        for id in results.keys():
            lot = results[id]
            lot_widget = QtWidgets.QListWidgetItem()
            font = QtGui.QFont()
            font.setPointSize(12)
            lot_widget.setFont(font)
            lot_widget.setText(f"id: {id}\nПродавец: {lot[0]}\nАдрес токена: {lot[1]}\nНазвание: {lot[4]}\nСимвол: {lot[5]}\nДесятичных токенов: {lot[6]}\nЦена за 1 единицу: {lot[2]} wei\nКоличество единиц: {lot[3]}\n")
            self.ui.results.addItem(lot_widget)


def main():
    app = QtWidgets.QApplication([])
    application = set_application(MainWindow())
    application.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

    with open('wallet.txt', 'r') as fl:
        w = fl.read()
        application.ui.wallet_label.setText(f"Кошелек: {w}")
        set_wallet(w)

    ids = lot_id()
    for i in range(1, ids + 1):
        lot = lot_info(i)
        if lot[3] > 0:
            application.lots[str(i)] = lot
            application.create_lot_widget(i, lot)

    application.ui.last_id.setText(f"Id последнего лота: {ids}")

    thread_list_lot.start()
    thread_cancel.start()
    thread_change_price.start()
    thread_purchase.start()

    application.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
