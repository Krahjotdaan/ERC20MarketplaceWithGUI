from keys import W3, WALLET_ADDRESS, PRIVATE_KEY, MARKETPLACE


def lot_id():
    id = MARKETPLACE.functions.lotId().call()
    print(f"lotId: {id}")


def lot_info():
    try:
        id = int(input("Введите id лота: "))
    except ValueError:
        id = int(input("Введите id лота: "))

    lot = MARKETPLACE.functions.list(id).call()
    print(f"Лот: {id}")
    print(f"Адрес токена: {lot[0]}")
    print(f"Продавец: {lot[0]}")
    print(f"Цена за 1 единицу: {lot[0]}")
    print(f"Количество единиц: {lot[0]}")


def list_lot():
    token_address = input("Введите адрес токена: ")

    try:
        price = int(input("Введите цену за 1 единицу в wei: "))
    except ValueError:
        price = int(input("Введите цену за 1 единицу в wei: "))

    try:
        amount = int(input("Введите количество единиц для продажи: "))
    except ValueError:
        amount = int(input("Введите количество единиц для продажи: "))

    transaction = MARKETPLACE.functions.listLot(token_address, price, amount).build_transaction({
        'from': WALLET_ADDRESS,
        'chainId': 17000,
        'gas': 300000,
        'maxFeePerGas': W3.eth.gas_price + 300000,
        'nonce': W3.eth.get_transaction_count(WALLET_ADDRESS)
    })
    signed_transaction = W3.eth.account.sign_transaction(transaction, PRIVATE_KEY)
    tx_hash = W3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    print(f"хэш транзакции: {W3.to_hex(tx_hash)}")


def cancel():
    try:
        id = int(input("Введите id лота: "))
    except ValueError:
        id = int(input("Введите id лота: "))

    try:
        amount = int(input("Введите количество единиц для снятия с продажи: "))
    except ValueError:
        amount = int(input("Введите количество единиц для снятия с продажи: "))

    transaction = MARKETPLACE.functions.cancel(id, amount).build_transaction({
        'from': WALLET_ADDRESS,
        'chainId': 17000,
        'gas': 300000,
        'maxFeePerGas': W3.eth.gas_price + 300000,
        'nonce': W3.eth.get_transaction_count(WALLET_ADDRESS)
    })
    signed_transaction = W3.eth.account.sign_transaction(transaction, PRIVATE_KEY)
    tx_hash = W3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    print(f"хэш транзакции: {W3.to_hex(tx_hash)}")


def change_price():
    try:
        id = int(input("Введите id лота: "))
    except ValueError:
        id = int(input("Введите id лота: "))

    try:
        new_price = int(input("Введите новую цену за 1 единицу токена в wei: "))
    except ValueError:
        new_price = int(input("Введите новую цену за 1 единицу токена в wei: "))

    transaction = MARKETPLACE.functions.changePrice(id, new_price).build_transaction({
        'from': WALLET_ADDRESS,
        'chainId': 17000,
        'gas': 300000,
        'maxFeePerGas': W3.eth.gas_price + 300000,
        'nonce': W3.eth.get_transaction_count(WALLET_ADDRESS)
    })
    signed_transaction = W3.eth.account.sign_transaction(transaction, PRIVATE_KEY)
    tx_hash = W3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    print(f"хэш транзакции: {W3.to_hex(tx_hash)}")


def purchase():
    try:
        id = int(input("Введите id лота: "))
    except ValueError:
        id = int(input("Введите id лота: "))

    try:
        amount = int(input("Введите количество единиц для покупки: "))
    except ValueError:
        amount = int(input("Введите количество единиц для покупки: "))

    try:
        value = int(input("Введите количество wei, которое хотите заплатить: "))
    except ValueError:
        value = int(input("Введите количество wei, которое хотите заплатить: "))

    transaction = MARKETPLACE.functions.cancel(id, amount).build_transaction({
        'from': WALLET_ADDRESS,
        'chainId': 17000,
        'gas': 300000,
        'maxFeePerGas': W3.eth.gas_price + 300000,
        'value': value,
        'nonce': W3.eth.get_transaction_count(WALLET_ADDRESS)
    })
    signed_transaction = W3.eth.account.sign_transaction(transaction, PRIVATE_KEY)
    tx_hash = W3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    print(f"хэш транзакции: {W3.to_hex(tx_hash)}")
