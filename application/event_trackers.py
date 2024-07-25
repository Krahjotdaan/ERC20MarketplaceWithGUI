import time
from threading import Thread
from application.keys import PRINT_EVENT, MARKETPLACE, APPLICATION


def log_loop_list_lot(event_filter, poll_interval):
    while True:
        while not PRINT_EVENT:
            time.sleep(poll_interval)
        for event in event_filter.get_new_entries():
            APPLICATION.ui.events_display.append(
                f"Новый лот\n \
                id лота: {event['args']['lotId']}\n \
                Продавец: {event['args']['owner']}\n \
                Адрес токена: {event['args']['tokenAddress']}\n \
                Цена за 1 единицу: {event['args']['price']}\n \
                Количество единиц: {event['args']['amount']}\n"
            )
        time.sleep(poll_interval)


def log_loop_cancel(event_filter, poll_interval):
    while True:
        while not PRINT_EVENT:
            time.sleep(poll_interval)
        for event in event_filter.get_new_entries():
            APPLICATION.ui.events_display.append(
                f"Отмена продажи\n \
                id лота: {event['args']['lotId']}\n \
                Количество единиц снятых с продажи: {event['args']['amount']}\n"
            )
        time.sleep(poll_interval)


def log_loop_change_price(event_filter, poll_interval):
    while True:
        while not PRINT_EVENT:
            time.sleep(poll_interval)
        for event in event_filter.get_new_entries():
            APPLICATION.ui.events_display.append(
                f"Изменена цена\n \
                id лота: {event['args']['lotId']}\n \
                Старая цена: {event['args']['oldPrice']}\n \
                Новая цена: {event['args']['newPrice']}\n"
            )
        time.sleep(poll_interval)


def log_loop_purchase(event_filter, poll_interval):
    while True:
        while not PRINT_EVENT:
            time.sleep(poll_interval)
        for event in event_filter.get_new_entries():
            APPLICATION.ui.events_display.append(
                f"Покупка\n \
                id лота: {event['args']['lotId']}\n \
                Адрес токена: {event['args']['tokenAddress']}\n \
                Цена за 1 единицу: {event['args']['price']}\n \
                Куплено единиц: {event['args']['amount']}\n \
                Покупатель: {event['args']['customer']}\n"
            )
        time.sleep(poll_interval)


event_filter_list_lot = MARKETPLACE.events.ListLot.create_filter(fromBlock="latest")
event_filter_cancel = MARKETPLACE.events.Cancel.create_filter(fromBlock="latest")
event_filter_change_price = MARKETPLACE.events.ChangePrice.create_filter(fromBlock="latest")
event_filter_purchase = MARKETPLACE.events.Purchase.create_filter(fromBlock="latest")

thread_list_lot = Thread(target=log_loop_list_lot, args=(event_filter_list_lot, 10))
thread_cancel = Thread(target=log_loop_cancel, args=(event_filter_cancel, 10))
thread_change_price = Thread(target=log_loop_change_price, args=(event_filter_change_price, 10))
thread_purchase = Thread(target=log_loop_purchase, args=(event_filter_purchase, 10))
