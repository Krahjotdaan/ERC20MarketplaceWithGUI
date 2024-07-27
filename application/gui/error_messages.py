from PyQt5.QtWidgets import QErrorMessage


def incorrect_id(parent):
    eras = QErrorMessage(parent=parent)
    eras.showMessage("Некорректный id")
    

def incorrect_wallet(parent):
    eras = QErrorMessage(parent=parent)
    eras.showMessage("Некорректный адрес кошелька")


def incorrect_private_key(parent):
    eras = QErrorMessage(parent=parent)
    eras.showMessage("Некорректный приватный ключ")


def incorrect_amount(parent):
    eras = QErrorMessage(parent=parent)
    eras.showMessage("Некорректное количество")


def incorrect_price(parent):
    eras = QErrorMessage(parent=parent)
    eras.showMessage("Некорректная цена")


def incorrect_address(parent):
    eras = QErrorMessage(parent=parent)
    eras.showMessage("Некорректный адрес")
