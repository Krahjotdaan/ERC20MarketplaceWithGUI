from application.keys import W3, MARKETPLACE, get_wallet
import web3


def lot_id():
    id = MARKETPLACE.functions.lotId().call()
    return id


def lot_info(id):
    lot = MARKETPLACE.functions.list(id).call()
    return lot


def list_lot(token_address, price, amount, PRIVATE_KEY):
    transaction = MARKETPLACE.functions.listLot(token_address, price, amount).build_transaction({
        'from': get_wallet(),
        'chainId': 17000,
        'gas': 1000000,
        'maxFeePerGas': W3.eth.gas_price + 1000000,
        'nonce': W3.eth.get_transaction_count(get_wallet())
    })
    signed_transaction = W3.eth.account.sign_transaction(transaction, PRIVATE_KEY)
    tx_hash = W3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    
    return W3.to_hex(tx_hash)


def cancel(id, amount, PRIVATE_KEY):
    transaction = MARKETPLACE.functions.cancel(id, amount).build_transaction({
        'from': get_wallet(),
        'chainId': 17000,
        'gas': 1000000,
        'maxFeePerGas': W3.eth.gas_price + 1000000,
        'nonce': W3.eth.get_transaction_count(get_wallet())
    })
    signed_transaction = W3.eth.account.sign_transaction(transaction, PRIVATE_KEY)
    tx_hash = W3.eth.send_raw_transaction(signed_transaction.rawTransaction)

    return W3.to_hex(tx_hash)


def change_price(id, new_price, PRIVATE_KEY):
    transaction = MARKETPLACE.functions.changePrice(id, new_price).build_transaction({
        'from': get_wallet(),
        'chainId': 17000,
        'gas': 1000000,
        'maxFeePerGas': W3.eth.gas_price + 1000000,
        'nonce': W3.eth.get_transaction_count(get_wallet())
    })
    signed_transaction = W3.eth.account.sign_transaction(transaction, PRIVATE_KEY)
    tx_hash = W3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    
    return W3.to_hex(tx_hash)


def purchase(id, amount, value, PRIVATE_KEY):
    transaction = MARKETPLACE.functions.purchase(id, amount).build_transaction({
        'from': get_wallet(),
        'chainId': 17000,
        'gas': 1000000,
        'maxFeePerGas': W3.eth.gas_price + 1000000,
        'value': value,
        'nonce': W3.eth.get_transaction_count(get_wallet())
    })
    print(transaction)
    signed_transaction = W3.eth.account.sign_transaction(transaction, PRIVATE_KEY)
    tx_hash = W3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    return W3.to_hex(tx_hash)
