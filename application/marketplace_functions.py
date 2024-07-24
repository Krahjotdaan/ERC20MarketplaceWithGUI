from keys import W3, WALLET_ADDRESS, MARKETPLACE


def lot_id():
    id = MARKETPLACE.functions.lotId().call()
    print(f"lotId: {id}")


def lot_info(id):
    lot = MARKETPLACE.functions.list(id).call()
    print(f"Лот: {id}")
    print(f"Адрес токена: {lot[0]}")
    print(f"Продавец: {lot[0]}")
    print(f"Цена за 1 единицу: {lot[0]}")
    print(f"Количество единиц: {lot[0]}")


def list_lot(token_address, price, amount, PRIVATE_KEY):
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


def cancel(id, amount, PRIVATE_KEY):
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


def change_price(id, new_price, PRIVATE_KEY):
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


def purchase(id, amount, value, PRIVATE_KEY):
    transaction = MARKETPLACE.functions.purchase(id, amount).build_transaction({
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
