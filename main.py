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
    """
    Главное окно приложения.

    Содержит все элементы UI и реализует логику работы приложения.
    """
    def __init__(self):
        """
        Инициализирует главное окно.
        """
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow() # Инициализирует UI из application.gui.MainWindow
        self.ui.setupUi(self) # Устанавливает UI

        # Инициализирует значок в трее
        self.tray_icon = QtWidgets.QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_ComputerIcon))

        # Создает действия для контекстного меню в трее
        show_action = QtWidgets.QAction("Развернуть", self)
        quit_action = QtWidgets.QAction("Выйти", self)
        hide_action = QtWidgets.QAction("Свернуть", self)

        # Подключает сигналы и слоты для действий
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(os._exit)

        # Создает контекстное меню для значка в трее
        tray_menu = QtWidgets.QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.setToolTip("ERC20Marketplace")
        self.tray_icon.show()

        # Инициализирует различные переменные приложения
        self.lots = {} # Словарь для хранения информации о лотах
        self.lot_widgets = {} # Словарь для хранения виджетов лотов
        self.my_lots_widgets = {} # Словарь для хранения виджетов лотов пользователя
        self.purchase_id = 0 # ID лота для покупки
        self.purchase_amount = 0 # Количество токенов для покупки
        self.purchase_cost = 0 # Итоговая стоимость покупки
        self.change_price_id = 0 # ID лота для изменения цены
        self.new_price = 0 # Новая цена лота
        self.cancel_id = 0 # ID лота для отмены продажи
        self.cancel_amount = 0 # Количество токенов для отмены
        self.remain_amount = 0 # Остаток токенов после отмены

    def closeEvent(self, event):
        """
        Переопределяет метод closeEvent, чтобы вместо закрытия окна скрыть его
        и показать сообщение в трее.
        """
        event.ignore() # Игнорирует событие закрытия
        self.hide() # Скрывает окно
        self.tray_icon.showMessage(
            "ERC20Marketplace", # Заголовок сообщения
            "Приложение свернуто в трей", # Текст сообщения
            QtWidgets.QSystemTrayIcon.Information, # Тип сообщения
            2000 # Время отображения сообщения в миллисекундах
        )
    
    def about_programm_button_click(self):
        """
        Обработчик события нажатия на кнопку "О программе".
        """
        self.about_programm_window = AboutProgrammWindow() # Создает окно "О программе"
        self.about_programm_window.setAttribute(QtCore.Qt.WA_DeleteOnClose, True) # Устанавливает, что окно будет удалено при закрытии
        self.about_programm_window.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint) # Устанавливает, что окно всегда будет поверх других окон
        self.about_programm_window.show() # Показывает окно

    def connect_wallet_button_click(self):
        """
        Обработчик события нажатия на кнопку "Подключить кошелек".
        """
        self.set_wallet_window = SetWalletWindow(self) # Создает окно "Подключить кошелек"
        self.set_wallet_window.setAttribute(QtCore.Qt.WA_DeleteOnClose, True) # Устанавливает, что окно будет удалено при закрытии
        self.set_wallet_window.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint) # Устанавливает, что окно всегда будет поверх других окон
        self.set_wallet_window.show() # Показывает окно

    def search_button_click(self):
        """
        Обработчик события нажатия на кнопку "Поиск".
        """
        self.search_window = SearchWindow(self) # Создает окно "Поиск"
        self.search_window.setAttribute(QtCore.Qt.WA_DeleteOnClose, True) # Устанавливает, что окно будет удалено при закрытии
        self.search_window.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint) 
        self.search_window.show() # Показывает окно

    def count_cost_button_click(self):
        """
        Обработчик события нажатия на кнопку "Рассчитать стоимость".

        Проверяет корректность введенных данных, рассчитывает стоимость покупки
        и выводит информацию о лоте и стоимости в `purchase_browser`.
        """
        try:
            # Проверяет корректность ID лота
            if int(self.ui.id_purchase_input.text()) > 0:
                self.purchase_id = int(self.ui.id_purchase_input.text())
            else:
                incorrect_id(self) # Вызывает функцию вывода ошибки
        except ValueError:
            incorrect_id(self) # Вызывает функцию вывода ошибки

        lot = None
        try:
            # Получает информацию о лоте из словаря `lots`
            lot = self.lots[str(self.purchase_id)] 

            # Проверяет корректность количества токенов
            if int(self.ui.amount_purchase_input.text()) > 0 and int(self.ui.amount_purchase_input.text()) <= lot[3]:
                self.purchase_amount = int(self.ui.amount_purchase_input.text())
                self.purchase_cost = self.purchase_amount * lot[2]
                # Выводит информацию о лоте и стоимости в `purchase_browser`
                self.ui.purchase_browser.setText(f"""id: {self.purchase_id}\nПродавец: {lot[0]}\nАдрес токена: {lot[1]}\nНазвание: {lot[4]}\nСимвол: {lot[5]}\nДесятичных токенов: {lot[6]}\nЦена за 1 единицу: {lot[2]} wei\nКоличество единиц: {self.purchase_amount}\nИтого: {self.purchase_cost} wei\n\nВставьте в поле ниже приватный ключ. Приватный ключ нужен для подписи отправляемых транзакций. Программа никак не сохраняет его и не передает третьим лицам. Нажмите кнопку "Подтвердить" для отправки транзакции.""")
                
                # Активирует поля для ввода приватного ключа и подтверждения покупки
                self.ui.apply_purchase_button.setEnabled(True)
                self.ui.private_key_input_purchase.setEnabled(True)
            else:
                incorrect_amount(self) # Вызывает функцию вывода ошибки
        
        except ValueError:
            incorrect_amount(self) # Вызывает функцию вывода ошибки 
       
        except KeyError:
            # Выводит сообщение об ошибке, если лот с указанным ID не найден
            eras = QtWidgets.QErrorMessage(parent=self)
            eras.showMessage("Такого id нет")        

    def apply_purchase_button_click(self):
        """
        Обработчик события нажатия на кнопку "Подтвердить" в окне покупки.

        Получает приватный ключ из поля ввода, отправляет транзакцию в блокчейн
        и выводит хэш в отдельное окно.
        """
        private_key = self.ui.private_key_input_purchase.text() # Получает приватный ключ
        
        try:
            # Вызывает функцию purchase для отправки транзакции
            tx_hash = purchase(self.purchase_id, self.purchase_amount, self.purchase_cost, private_key)
            
            # Создает окно для отображения хэша транзакции
            self.tx_browser = TxBrowser(tx_hash)
            self.tx_browser.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
            self.tx_browser.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            self.tx_browser.setFocus()
            self.tx_browser.show()

        except web3.exceptions.Web3ValidationError:
            # Обрабатывает исключение, которое может возникнуть при ошибке валидации
            pass  

        except web3.exceptions.InvalidAddress:
            # Обрабатывает исключение, которое может возникнуть при неверном адресе кошелька
            incorrect_wallet(self) # Вызывает функцию вывода ошибки

        except TypeError:
            # Обрабатывает исключение, которое может возникнуть при некорректном приватном ключе
            incorrect_private_key(self) # Вызывает функцию вывода ошибки

        except ValueError:
             # Обрабатывает исключение, которое может возникнуть при ошибке сети
            eras = QtWidgets.QErrorMessage(parent=self)
            eras.showMessage("Ошибка сети. Транзакция не отправлена")
        
        # Очищает поля ввода и отключает кнопку "Подтвердить"
        del private_key # Удаляет приватный ключ из памяти
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
        """
        Обработчик события нажатия на кнопку "Подтвердить" в окне продажи.

        Получает информацию о токенах, цену, количество и приватный ключ,
        отправляет транзакцию в блокчейн и выводит результат в отдельное окно.
        """
        token_address = None
        price = 0
        amount = 0
        private_key = None

        try:
            # Проверяет корректность адреса токена
            if self.ui.address_sell_input.text()[:2] == "0x":
                token_address = self.ui.address_sell_input.text()
            else:
                incorrect_address(self) # Вызывает функцию вывода ошибки
        except:
            incorrect_address(self) # Вызывает функцию вывода ошибки

        try:
            # Проверяет корректность цены
            if int(self.ui.price_sell_input.text()) > 0:
                price = int(self.ui.price_sell_input.text())
            else:
                incorrect_price(self) # Вызывает функцию вывода ошибки
        except ValueError:
            incorrect_price(self) # Вызывает функцию вывода ошибки

        try:
            # Проверяет корректность количества
            if int(self.ui.amount_sell_input.text()) > 0:
                amount = int(self.ui.amount_sell_input.text())
            else:
                incorrect_amount(self) # Вызывает функцию вывода ошибки
        except ValueError:
            incorrect_amount(self) # Вызывает функцию вывода ошибки

        private_key = self.ui.private_key_input_sell.text() # Получает приватный ключ
        
        try:
            # Вызывает функцию list_lot для отправки транзакции
            tx_hash = list_lot(token_address, price, amount, private_key)
            
            # Создает окно для отображения хэша транзакции
            self.tx_browser = TxBrowser(tx_hash)
            self.tx_browser.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
            self.tx_browser.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            self.tx_browser.setFocus()
            self.tx_browser.show()

        except web3.exceptions.Web3ValidationError:
            # Обрабатывает исключение, которое может возникнуть при ошибке валидации
            pass

        except web3.exceptions.InvalidAddress:
            # Обрабатывает исключение, которое может возникнуть при неверном адресе кошелька
            incorrect_wallet(self)

        except ValueError:
            # Обрабатывает исключение, которое может возникнуть при некорректном приватном ключе
            incorrect_private_key(self)
        
        except TypeError:
            # Обрабатывает исключение, которое может возникнуть при некорректном приватном ключе
            incorrect_private_key(self)
        
        # Очищает поля ввода и отключает кнопку "Подтвердить"
        del private_key # Удаляет приватный ключ из памяти
        self.ui.address_sell_input.setText("")
        self.ui.price_sell_input.setText("")
        self.ui.amount_sell_input.setText("")
        self.ui.private_key_input_sell.setText("")

    def count_new_price_button_click(self):
        """
        Обработчик события нажатия на кнопку "Рассчитать новую цену".

        Проверяет корректность введенных данных, вычисляет новую цену
        и выводит информацию о лоте и новой цене в `change_price_browser`.
        """
        try:
            # Проверяет корректность ID лота
            if int(self.ui.id_change_price_input.text()) > 0:
                self.change_price_id = int(self.ui.id_change_price_input.text())
            else:
                incorrect_id(self) # Вызывает функцию вывода ошибки
        except ValueError:
            incorrect_id(self) # Вызывает функцию вывода ошибки

        lot = None
        try:
            # Получает информацию о лоте из словаря `lots`
            lot = self.lots[str(self.change_price_id)]

            # Проверяет корректность новой цены
            if int(self.ui.price_change_price_input.text()) > 0 and int(self.ui.price_change_price_input.text()) != lot[3]:
                self.new_price = int(self.ui.price_change_price_input.text())
                
                # Выводит информацию о лоте и новой цене в `change_price_browser`
                self.ui.change_price_browser.setText(f"""id: {self.change_price_id}\nАдрес токена: {lot[1]}\nНазвание: {lot[4]}\nСимвол: {lot[5]}\nДесятичных токенов: {lot[6]}\nСтарая цена: {lot[2]} wei\nНовая цена: {self.new_price} wei\n\n\n\nВставьте в поле ниже приватный ключ. Приватный ключ нужен для подписи отправляемых транзакций. Программа никак не сохраняет его и не передает третьим лицам. Нажмите кнопку "Подтвердить" для отправки транзакции.""")
                
                # Активирует поля для ввода приватного ключа и подтверждения изменения цены
                self.ui.apply_change_price_button.setEnabled(True)
                self.ui.private_key_input_change_price.setEnabled(True)
            else:
                incorrect_price(self) # Вызывает функцию вывода ошибки

        except ValueError:
            incorrect_price(self) # Вызывает функцию вывода ошибки

        except KeyError:
            # Выводит сообщение об ошибке, если лот с указанным ID не найден
            eras = QtWidgets.QErrorMessage(parent=self)
            eras.showMessage("Такого id нет")

    def apply_change_price_button_click(self):
        """
        Обработчик события нажатия на кнопку "Подтвердить" в окне изменения цены.

        Получает приватный ключ из поля ввода, отправляет транзакцию в блокчейн
        и выводит хэш в отдельное окно.
        """
        private_key = self.ui.private_key_input_change_price.text() # Получает приватный ключ
        
        try:
            # Вызывает функцию change_price для отправки транзакции
            tx_hash = change_price(self.change_price_id, self.new_price, private_key)
            
            # Создает окно для отображения хэша транзакции
            self.tx_browser = TxBrowser(tx_hash)
            self.tx_browser.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
            self.tx_browser.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            self.tx_browser.setFocus()
            self.tx_browser.show()

        except web3.exceptions.Web3ValidationError:
            # Обрабатывает исключение, которое может возникнуть при ошибке валидации
            pass

        except web3.exceptions.InvalidAddress:
            # Обрабатывает исключение, которое может возникнуть при неверном адресе кошелька
            incorrect_wallet(self)

        except ValueError:
            # Обрабатывает исключение, которое может возникнуть при некорректном приватном ключе
            incorrect_private_key(self)

        except TypeError:
            # Обрабатывает исключение, которое может возникнуть при некорректном приватном ключе
            incorrect_private_key(self)
        
        # Очищает поля ввода и отключает кнопку "Подтвердить"
        del private_key # Удаляет приватный ключ из памяти
        self.change_price_id = 0
        self.new_price = 0
        self.ui.id_change_price_input.setText("")
        self.ui.price_change_price_input.setText("")
        self.ui.private_key_input_change_price.setText("")
        self.ui.apply_change_price_button.setEnabled(False)
        self.ui.private_key_input_change_price.setEnabled(False)
        self.ui.change_price_browser.setText(f"""id:\nАдрес токена:\nНазвание:\nСимвол:\nДесятичных токенов:\nСтарая цена:\nНовая цена:\n\n\n\nВставьте в поле ниже приватный ключ. Приватный ключ нужен для подписи отправляемых транзакций. Программа никак не сохраняет его и не передает третьим лицам. Нажмите кнопку "Подтвердить" для отправки транзакции.""")

    def count_cancel_button_click(self):
        """
        Обработчик события нажатия на кнопку "Рассчитать отмену".

        Проверяет корректность введенных данных, рассчитывает остаток токенов
        и выводит информацию о лоте и отмене в `cancel_browser`.
        """
        try:
            # Проверяет корректность ID лота
            if int(self.ui.id_cancel_input.text()) > 0:
                self.cancel_id = int(self.ui.id_cancel_input.text())
            else:
                incorrect_id(self) # Вызывает функцию вывода ошибки
        except ValueError:
            incorrect_id(self) # Вызывает функцию вывода ошибки

        lot = None
        try:
            # Получает информацию о лоте из словаря `lots`
            lot = self.lots[str(self.cancel_id)]

            # Проверяет корректность количества токенов для отмены
            if int(self.ui.amount_cancel_input.text()) > 0 and int(self.ui.amount_cancel_input.text()) <= lot[3]:
                self.cancel_amount = int(self.ui.amount_cancel_input.text()) # Рассчитывает остаток токенов
                
                # Выводит информацию о лоте и отмене в `cancel_browser`
                self.ui.cancel_browser.setText(f"""id: {self.cancel_id}\nАдрес токена: {lot[1]}\nНазвание: {lot[4]}\nСимвол: {lot[5]}\nДесятичных токенов: {lot[6]}\nЦена за 1 единицу: {lot[2]} wei\nБудет снято с продажи(ед. токенов): {self.cancel_amount}\nОстанется в продаже: {lot[3] - self.cancel_amount}\n\n\nВставьте в поле ниже приватный ключ. Приватный ключ нужен для подписи отправляемых транзакций. Программа никак не сохраняет его и не передает третьим лицам. Нажмите кнопку "Подтвердить" для отправки транзакции.""")
                
                # Активирует поля для ввода приватного ключа и подтверждения отмены
                self.ui.apply_cancel_button.setEnabled(True)
                self.ui.private_key_input_cancel.setEnabled(True)
            else:
                incorrect_amount(self) # Вызывает функцию вывода ошибки
        except ValueError:
            incorrect_amount(self) # Вызывает функцию вывода ошибки
        
        except KeyError:
            # Выводит сообщение об ошибке, если лот с указанным ID не найден
            eras = QtWidgets.QErrorMessage(parent=self)
            eras.showMessage("Такого id нет")

    def apply_cancel_button_click(self):
        """
        Обработчик события нажатия на кнопку "Подтвердить" в окне отмены продажи.

        Получает приватный ключ из поля ввода, отправляет транзакцию в блокчейн
        и выводит хэш в отдельное окно.
        """
        private_key = self.ui.private_key_input_cancel.text() # Получает приватный ключ
        
        try:
            # Вызывает функцию cancel для отправки транзакции
            tx_hash = cancel(self.cancel_id, self.cancel_amount, private_key)
            
            # Создает окно для отображения хэша транзакции
            self.tx_browser = TxBrowser(tx_hash)
            self.tx_browser.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
            self.tx_browser.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            self.tx_browser.setFocus()
            self.tx_browser.show()

        except web3.exceptions.Web3ValidationError:
            # Обрабатывает исключение, которое может возникнуть при ошибке валидации
            pass

        except web3.exceptions.InvalidAddress:
            # Обрабатывает исключение, которое может возникнуть при неверном адресе кошелька
            incorrect_wallet(self)

        except ValueError:
            # Обрабатывает исключение, которое может возникнуть при некорректном приватном ключе
            incorrect_private_key(self)

        except TypeError:
            # Обрабатывает исключение, которое может возникнуть при некорректном приватном ключе            
            incorrect_private_key(self)

        # Очищает поля ввода и отключает кнопку "Подтвердить"   
        del private_key # Удаляет приватный ключ из памяти
        self.cancel_id = 0
        self.cancel_amount = 0
        self.ui.id_cancel_input.setText("")
        self.ui.amount_cancel_input.setText("")
        self.ui.private_key_input_cancel.setText("")
        self.ui.apply_cancel_button.setEnabled(False)
        self.ui.private_key_input_cancel.setEnabled(False)
        self.ui.cancel_browser.setText(f"""id:\nАдрес токена:\nНазвание:\nСимвол:\nДесятичных токенов:\nЦена за 1 единицу:wei\nБудет снято с продажи(ед. токенов):\nОстанется в продаже:\n\n\nВставьте в поле ниже приватный ключ. Приватный ключ нужен для подписи отправляемых транзакций. Программа никак не сохраняет его и не передает третьим лицам. Нажмите кнопку "Подтвердить" для отправки транзакции.""")

    def logs_journal_button_click(self):
        """
        Обработчик события нажатия на кнопку "Журнал логов".

        Открывает файл "logs.log" в системном текстовом редакторе.
        Если файл не существует, создает его и открывает.
        """
        try:
            os.startfile("logs.log") # Пытается открыть файл "logs.log"
        except FileNotFoundError:
            # Если файл не найден, создает его и открывает
            open("logs.log", 'a').close() # Создает файл, если он не существует
            os.startfile("logs.log")
    
    def create_lot_widget(self, id, lot):
        """
        Создает виджет для лота и добавляет его в список лотов.
        """
        lot_widget = QtWidgets.QListWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(12)
        lot_widget.setFont(font)
        lot_widget.setText(f"id: {id}\nПродавец: {lot[0]}\nАдрес токена: {lot[1]}\nНазвание: {lot[4]}\nСимвол: {lot[5]}\nДесятичных токенов: {lot[6]}\nЦена за 1 единицу: {lot[2]} wei\nКоличество единиц: {lot[3]}\n")
        self.lot_widgets[str(id)] = lot_widget
        self.ui.list_all_lots.addItem(lot_widget)

        # Добавляет лот в список лотов текущего пользователя, если владелец лота - это текущий пользователь
        if lot[0] == get_wallet():
            my_lot_widget = QtWidgets.QListWidgetItem()
            my_lot_widget.setFont(font)
            my_lot_widget.setText(f"id: {id}\nПродавец: {lot[0]}\nАдрес токена: {lot[1]}\nНазвание: {lot[4]}\nСимвол: {lot[5]}\nДесятичных токенов: {lot[6]}\nЦена за 1 единицу: {lot[2]} wei\nКоличество единиц: {lot[3]}\n")
            self.my_lots_widgets[str(id)] = my_lot_widget
            self.ui.list_my_lots.addItem(my_lot_widget)


class AboutProgrammWindow(QtWidgets.QMainWindow):
    """
    Окно "О программе"
    """
    def __init__(self):
        """
        Инициализирует окно
        """
        super(AboutProgrammWindow, self).__init__()
        self.ui = Ui_AboutProgramm()
        self.ui.setupUi(self)


class SetWalletWindow(QtWidgets.QDialog):
    """
    Класс для окна установки кошелька.
    """
    def __init__(self, root : MainWindow):
        """
        Инициализирует окно установки кошелька.
        """
        super(SetWalletWindow, self).__init__()
        self.ui = Ui_SetWallet()
        self.ui.setupUi(self)
        self.main = root

    def accept(self):
        """
        Обработка нажатия кнопки "ОК".

        Проверяет введенный адрес кошелька, устанавливает его в приложении,
        обновляет список лотов пользователя и закрывает окно.
        """
        try:
            # Проверяет корректность адреса
            if self.ui.wallet_input.text()[:2] == "0x":
                set_wallet(self.ui.wallet_input.text())
                self.main.ui.wallet_label.setText(f"Кошелек: {self.ui.wallet_input.text()}")

                # Записывает новый кошелек в файл
                with open('wallet.txt', 'w') as fl:
                    fl.write(self.ui.wallet_input.text())

                # Очищает список лотов старого кошелькм
                self.main.ui.list_my_lots.clear()
                self.main.my_lots_widgets.clear()

                # Обновляет список лотов и создает новые виджеты
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
                incorrect_wallet(self) # Вызывает функцию вывода ошибки
        except:
            incorrect_wallet(self) # Вызывает функцию вывода ошибки

    def decline(self):
        """
        Обработка нажатия кнопки "Отмена".

        Закрывает окно.
        """
        self.close()


class TxBrowser(QtWidgets.QMainWindow):
    """
    Класс окна для вывода транзакции
    """
    def __init__(self, tx_hash):
        """
        Инициализирует окно
        """
        super(TxBrowser, self).__init__()
        self.ui = Ui_TxBrowser()
        self.ui.setupUi(self)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.ui.tx_info.setFont(font)
        self.ui.tx_info.setText(f"Хэш транзакции: {tx_hash}\nПолная информация: https://holesky.etherscan.io/tx/{tx_hash}")


class SearchWindow(QtWidgets.QMainWindow):
    """
    Класс окна поиска
    """
    def __init__(self, root : MainWindow):
        """
        Инициализирует окно поиска
        """
        super(SearchWindow, self).__init__()
        self.ui = Ui_SearchWindow()
        self.ui.setupUi(self)
        self.main = root

    def by_id_button_click(self):
        """
        Поиск по ID
        """
        results = {}
        try:
            # Проверяет корректность ID
            if int(self.ui.by_id_input.text()) > 0:
                # Получает лот из словаря
                id = int(self.ui.by_id_input.text())
                lot = self.main.lots[str(id)]
                results[str(id)] = lot
                self.show_results(id, results) # Вызывает окно с результатами поиска
            else:
                incorrect_id(self) # Вызывает функцию вывода ошибки
        except ValueError:
            incorrect_id(self) # Вызывает функцию вывода ошибки

        except KeyError:
            # Выводит сообщение об ошибке, если лот с указанным ID не найден
            eras = QtWidgets.QErrorMessage(parent=self)
            eras.showMessage("Такого id нет")

    def by_address_button_click(self):
        """
        Поиск по адресу токена
        """
        results = {}
        address = ""
        try:
            # Проверяет корректность адреса
            if self.ui.by_address_input.text()[:2] == "0x":
                address = self.ui.by_address_input.text()
                # Получает все лоты с указаным адресом
                for key in self.main.lots.keys():
                    if self.main.lots[key][1] == address:
                        results[key] = self.main.lots[key]
            else:
                incorrect_address(self) # Вызывает функцию вывода ошибки
        except:
            incorrect_address(self) # Вызывает функцию вывода ошибки
        
        if len(results.keys()) == 0:
            # Показывает сообщение, если ничего не найдено
            eras = QtWidgets.QErrorMessage(parent=self)
            eras.showMessage("Ничего не найдено")
        else:
            # Вызывает окно с результатами поиска
            self.show_results(address, results)

    def by_name_button_click(self):
        """
        Поиск по названию токена
        """
        results = {}
        name = ""
        try:
            name = self.ui.by_name_input.text()
            # Получает все лоты с указаным названием
            for key in self.main.lots.keys():
                if self.main.lots[key][4] == name:
                    results[key] = self.main.lots[key]
        except:
            eras = QtWidgets.QErrorMessage(parent=self)
            eras.showMessage("Некорректное название")
        
        if len(results.keys()) == 0:
            # Показывает сообщение, если ничего не найдено
            eras = QtWidgets.QErrorMessage(parent=self)
            eras.showMessage("Ничего не найдено")
        else:
            # Вызывает окно с результатами поиска
            self.show_results(name, results)

    def show_results(self, template, results):
        """
        Функция вызова окна с результатами поиска
        """
        self.search_results_window = SearchResultsWindow(template, results)
        self.search_results_window.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.search_results_window.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.search_results_window.show()


class SearchResultsWindow(QtWidgets.QMainWindow):
    """
    Класс окна результатов поиска
    """
    def __init__(self, template, results : dict):
        """
        Инициализирует окно результатов поиска
        """
        super(SearchResultsWindow, self).__init__()
        self.ui = Ui_SearchResults()
        self.ui.setupUi(self)
        self.results = results
        self.ui.label.setText(f"""Результаты поиска по "{str(template)}" """)

        # Для каждого найденого лота создает виджет
        for id in results.keys():
            lot = results[id]
            lot_widget = QtWidgets.QListWidgetItem()
            font = QtGui.QFont()
            font.setPointSize(12)
            lot_widget.setFont(font)
            lot_widget.setText(f"id: {id}\nПродавец: {lot[0]}\nАдрес токена: {lot[1]}\nНазвание: {lot[4]}\nСимвол: {lot[5]}\nДесятичных токенов: {lot[6]}\nЦена за 1 единицу: {lot[2]} wei\nКоличество единиц: {lot[3]}\n")
            self.ui.results.addItem(lot_widget)


def main():
    """
    Точка входа в приложение.

    Инициализирует приложение, устанавливает кошелек, загружает лоты,
    запускает фоновые потоки и отображает главное окно.
    """
    app = QtWidgets.QApplication([]) # Инициализирует приложение
    application = set_application(MainWindow()) # Инициализирует главное окно
    application.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

    # Загрузка и установка адреса кошелька из файла
    with open('wallet.txt', 'r') as fl:
        w = fl.read()
        application.ui.wallet_label.setText(f"Кошелек: {w}")
        set_wallet(w)

    # Загрузка информации о лотах
    ids = lot_id()
    for i in range(1, ids + 1):
        lot = lot_info(i)
        if lot[3] > 0:
            application.lots[str(i)] = lot # Сохранение информации о лоте в словарь
            application.create_lot_widget(i, lot) # Создание виджета лота

    application.ui.last_id.setText(f"Id последнего лота: {ids}") # Обновление label с ID последнего лота

    # Запуск потоков отслеживания событий
    thread_list_lot.start()
    thread_cancel.start()
    thread_change_price.start()
    thread_purchase.start()

    application.show() # Отображение главного окна

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
