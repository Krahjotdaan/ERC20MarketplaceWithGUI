from application.keys import W3, MARKETPLACE, get_wallet
from application.logger import *


def lot_id():
    """
    Функция для получения последнего ID лота, созданного на маркетплейсе.

    :return: Последний ID лота.
    :rtype: int
    """
    id = MARKETPLACE.functions.lotId().call()
    return id


def lot_info(id):
    """
    Функция для получения информации о лоте по его ID.

    :param id: ID лота.
    :type id: int

    :return: Информация о лоте.
    :rtype: dict
    """
    lot = MARKETPLACE.functions.list(id).call()
    return lot


def list_lot(token_address, price, amount, PRIVATE_KEY):
    """
    Функция для вызова контракта ListLot с целью размещения лота на маркетплейсе.

    :param token_address: Адрес токена, который будет выставлен на продажу.
    :type token_address: str
    :param price: Цена лота в wei (1 ETH = 1 000 000 000 000 000 000 wei).
    :type price: int
    :param amount: Количество токенов, которые будут выставлены на продажу.
    :type amount: int
    :param PRIVATE_KEY: Приватный ключ аккаунта, который будет использовать для подписи транзакции.
    :type PRIVATE_KEY: str

    :return: Присвоенный хэш отправленной транзакции
    :rtype: str
    """
    transaction = MARKETPLACE.functions.listLot(token_address, price, amount).build_transaction({
        'from': get_wallet(), # Получает адрес кошелька
        'chainId': 17000, # Устанавливает ID сети Holesky
        'gas': 1000000, # Устанавливает максимальное количество газа
        'maxFeePerGas': W3.eth.gas_price + 1000000, # Устанавливает максимальную цену газа
        'nonce': W3.eth.get_transaction_count(get_wallet()) # Получает nonce для транзакции
    })
    signed_transaction = W3.eth.account.sign_transaction(transaction, PRIVATE_KEY) # Подписывает транзакцию
    tx_hash = W3.eth.send_raw_transaction(signed_transaction.rawTransaction) # Отправляет транзакцию
    add_log(f"Вызвана функция list_lot()\nПараметры:\nАдрес токена: {token_address}\nЦена: {price}\nКоличество: {amount}\nХэш транзакции: {W3.to_hex(tx_hash)}\n")
    
    return W3.to_hex(tx_hash) # Возвращает хэш транзакции


def cancel(id, amount, PRIVATE_KEY):
    """
    Функция для отмены продажи лота на маркетплейсе.

    :param id: ID лота, который нужно отменить.
    :type id: int
    :param amount: Количество токенов, которые нужно отменить.
    :type amount: int
    :param PRIVATE_KEY: Приватный ключ аккаунта, который будет использовать для подписи транзакции.
    :type PRIVATE_KEY: str

    :return: Присвоенный хэш отправленной транзакции
    :rtype: str
    """
    transaction = MARKETPLACE.functions.cancel(id, amount).build_transaction({
        'from': get_wallet(), # Получает адрес кошелька
        'chainId': 17000, # Устанавливает ID сети Holesky
        'gas': 1000000, # Устанавливает максимальное количество газа
        'maxFeePerGas': W3.eth.gas_price + 1000000, # Устанавливает максимальную цену газа
        'nonce': W3.eth.get_transaction_count(get_wallet()) # Получает nonce для транзакции
    })
    signed_transaction = W3.eth.account.sign_transaction(transaction, PRIVATE_KEY) # Подписывает транзакцию
    tx_hash = W3.eth.send_raw_transaction(signed_transaction.rawTransaction) # Отправляет транзакцию
    add_log(f"Вызвана функция cancel()\nПараметры:\nid: {id}\nКоличество: {amount}\nХэш транзакции: {W3.to_hex(tx_hash)}\n")

    return W3.to_hex(tx_hash) # Возвращает хэш транзакции


def change_price(id, new_price, PRIVATE_KEY):
    """
    Функция для изменения цены лота на маркетплейсе.

    :param id: ID лота, для которого нужно изменить цену.
    :type id: int
    :param new_price: Цена лота в wei (1 ETH = 1 000 000 000 000 000 000 wei).
    :type new_price: int
    :param PRIVATE_KEY: Приватный ключ аккаунта, который будет использовать для подписи транзакции.
    :type PRIVATE_KEY: str

    :return: Присвоенный хэш отправленной транзакции
    :rtype: str
    """
    transaction = MARKETPLACE.functions.changePrice(id, new_price).build_transaction({
        'from': get_wallet(), # Получает адрес кошелька
        'chainId': 17000, # Устанавливает ID сети Holesky
        'gas': 1000000, # Устанавливает максимальное количество газа
        'maxFeePerGas': W3.eth.gas_price + 1000000, # Устанавливает максимальную цену газа
        'nonce': W3.eth.get_transaction_count(get_wallet()) # Получает nonce для транзакции
    })
    signed_transaction = W3.eth.account.sign_transaction(transaction, PRIVATE_KEY) # Подписывает транзакцию
    tx_hash = W3.eth.send_raw_transaction(signed_transaction.rawTransaction) # Отправляет транзакцию
    add_log(f"Вызвана функция change_price()\nПараметры:\nid: {id}\nНовая цена: {new_price}\nХэш транзакции: {W3.to_hex(tx_hash)}\n")
    
    return W3.to_hex(tx_hash) # Возвращает хэш транзакции


def purchase(id, amount, value, PRIVATE_KEY):
    """
    Функция для покупки лота на маркетплейсе.

    :param id: ID лота, который нужно купить.
    :type id: int
    :param amount: Количество токенов, которые нужно купить.
    :type amount: int
    :param value: Сумма в wei (1 ETH = 1 000 000 000 000 000 000 wei), которая будет отправлена продавцу.
    :type value: int
    :param PRIVATE_KEY: Приватный ключ аккаунта, который будет использовать для подписи транзакции.
    :type PRIVATE_KEY: str

    :return: Присвоенный хэш отправленной транзакции
    :rtype: str
    """
    transaction = MARKETPLACE.functions.purchase(id, amount).build_transaction({
        'from': get_wallet(), # Получает адрес кошелька
        'chainId': 17000, # Устанавливает ID сети Holesky
        'gas': 1000000, # Устанавливает максимальное количество газа
        'maxFeePerGas': W3.eth.gas_price + 1000000, # Устанавливает максимальную цену газа
        'value': value, # Устанавливает сумму в wei, которая будет отправлена продавцу
        'nonce': W3.eth.get_transaction_count(get_wallet()) # Получает nonce для транзакции
    })
    signed_transaction = W3.eth.account.sign_transaction(transaction, PRIVATE_KEY) # Подписывает транзакцию
    tx_hash = W3.eth.send_raw_transaction(signed_transaction.rawTransaction) # Отправляет транзакцию
    add_log(f"Вызвана функция purchase()\nПараметры:\nid: {id}\nКоличество: {amount}\nПередано эфира: {value} wei\nХэш транзакции: {W3.to_hex(tx_hash)}\n")

    return W3.to_hex(tx_hash) # Возвращает хэш транзакции
