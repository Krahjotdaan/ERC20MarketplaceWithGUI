from keys import W3, WALLET_ADDRESS, PRIVATE_KEY, MARKETPLACE


def lot_id():
    id = MARKETPLACE.functions.lotId().call()
    print(f"lotId: {id}")


def lot_info():
    id = int(input("Введите id лота: "))
    lot = MARKETPLACE.functions.list(id).call()
    print(f"Лот: {id}")
    print(f"Адрес токена: {lot[0]}")
    print(f"Продавец: {lot[0]}")
    print(f"Цена за 1 единицу: {lot[0]}")
    print(f"Количество единиц: {lot[0]}")


def list_lot():
    token_address = input("Введите адрес токена: ")
    price = input("Введите цену за 1 единицу в wei: ")
    amount = input("Введите количество единиц для продажи: ")

    transaction = MARKETPLACE.functions.listLot(token_address, price, amount).build_transaction({
        'from': WALLET_ADDRESS,
        'chainId': 11155111,
        'gas': 300000,
        'maxFeePerGas': W3.eth.gas_price + 300000,
        'nonce': W3.eth.get_transaction_count(WALLET_ADDRESS)
    })
    signed_transaction = W3.eth.account.sign_transaction(transaction, PRIVATE_KEY)
    tx_hash = W3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    print(f"хэш транзакции: {W3.to_hex(tx_hash)}")


def cancel():
    id = int(input("Введите id лота: "))
    amount = int(input("Введите количество единиц для снятия с продажи: "))

    transaction = MARKETPLACE.functions.cancel(id, amount).build_transaction({
        'from': WALLET_ADDRESS,
        'chainId': 11155111,
        'gas': 300000,
        'maxFeePerGas': W3.eth.gas_price + 300000,
        'nonce': W3.eth.get_transaction_count(WALLET_ADDRESS)
    })
    signed_transaction = W3.eth.account.sign_transaction(transaction, PRIVATE_KEY)
    tx_hash = W3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    print(f"хэш транзакции: {W3.to_hex(tx_hash)}")


def change_price():
    id = int(input("Введите id лота: "))
    new_price = int(input("Введите новую цену за 1 единицу токена в wei: ")
)
    transaction = MARKETPLACE.functions.changePrice(id, new_price).build_transaction({
        'from': WALLET_ADDRESS,
        'chainId': 11155111,
        'gas': 300000,
        'maxFeePerGas': W3.eth.gas_price + 300000,
        'nonce': W3.eth.get_transaction_count(WALLET_ADDRESS)
    })
    signed_transaction = W3.eth.account.sign_transaction(transaction, PRIVATE_KEY)
    tx_hash = W3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    print(f"хэш транзакции: {W3.to_hex(tx_hash)}")


def purchase():
    id = int(input("Введите id лота: "))
    amount = int(input("Введите количество единиц для покупки: "))
    value = int(input("Введите количество wei, которое хотите заплатить: "))

    transaction = MARKETPLACE.functions.cancel(id, amount).build_transaction({
        'from': WALLET_ADDRESS,
        'chainId': 11155111,
        'gas': 300000,
        'maxFeePerGas': W3.eth.gas_price + 300000,
        'value': value,
        'nonce': W3.eth.get_transaction_count(WALLET_ADDRESS)
    })
    signed_transaction = W3.eth.account.sign_transaction(transaction, PRIVATE_KEY)
    tx_hash = W3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    print(f"хэш транзакции: {W3.to_hex(tx_hash)}")
    