import time
from threading import Thread
from application.keys import PRINT_EVENT, MARKETPLACE, APPLICATION


def log_loop_list_lot(event_filter, poll_interval):
    while True:
        while not PRINT_EVENT:
            time.sleep(poll_interval)
        try:
            for event in event_filter.get_new_entries():
                APPLICATION.ui.events_display.append(
                    f"Новый лот\nid лота: {event['args']['lotId']}\nПродавец: {event['args']['owner']}\nАдрес токена: {event['args']['tokenAddress']}\nЦена за 1 единицу: {event['args']['price']}\nКоличество единиц: {event['args']['amount']}\n"
                )
            time.sleep(poll_interval)
        except:
            event_filter = MARKETPLACE.events.ListLot.create_filter(fromBlock="latest")


def log_loop_cancel(event_filter, poll_interval):
    while True:
        while not PRINT_EVENT:
            time.sleep(poll_interval)
        try:
            for event in event_filter.get_new_entries():
                APPLICATION.ui.events_display.append(
                    f"Отмена продажи\nid лота: {event['args']['lotId']}\nКоличество единиц снятых с продажи: {event['args']['amount']}\n"
                )
            time.sleep(poll_interval)
        except:
            event_filter = MARKETPLACE.events.Cancel.create_filter(fromBlock="latest")


def log_loop_change_price(event_filter, poll_interval):
    while True:
        while not PRINT_EVENT:
            time.sleep(poll_interval)
        try:
            for event in event_filter.get_new_entries():
                APPLICATION.ui.events_display.append(
                    f"Изменена цена\nid лота: {event['args']['lotId']}\nСтарая цена: {event['args']['oldPrice']}\nНовая цена: {event['args']['newPrice']}\n"
                )
            time.sleep(poll_interval)
        except:
            event_filter = MARKETPLACE.events.ChangePrice.create_filter(fromBlock="latest")


def log_loop_purchase(event_filter, poll_interval):
    while True:
        while not PRINT_EVENT:
            time.sleep(poll_interval)
        try:
            for event in event_filter.get_new_entries():
                APPLICATION.ui.events_display.append(
                    f"Покупка\nid лота: {event['args']['lotId']}\nАдрес токена: {event['args']['tokenAddress']}\nЦена за 1 единицу: {event['args']['price']}\nКуплено единиц: {event['args']['amount']}\nПокупатель: {event['args']['customer']}\n"
                )
            time.sleep(poll_interval)
        except:
            event_filter = MARKETPLACE.events.Purchase.create_filter(fromBlock="latest")


event_filter_list_lot = MARKETPLACE.events.ListLot.create_filter(fromBlock="latest")
event_filter_cancel = MARKETPLACE.events.Cancel.create_filter(fromBlock="latest")
event_filter_change_price = MARKETPLACE.events.ChangePrice.create_filter(fromBlock="latest")
event_filter_purchase = MARKETPLACE.events.Purchase.create_filter(fromBlock="latest")

thread_list_lot = Thread(target=log_loop_list_lot, args=(event_filter_list_lot, 10))
thread_cancel = Thread(target=log_loop_cancel, args=(event_filter_cancel, 10))
thread_change_price = Thread(target=log_loop_change_price, args=(event_filter_change_price, 10))
thread_purchase = Thread(target=log_loop_purchase, args=(event_filter_purchase, 10))
