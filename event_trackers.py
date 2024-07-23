import time
from keys import PRINT_EVENT, MARKETPLACE


def log_loop_list_lot(event_filter, poll_interval):
    while True:
        while not PRINT_EVENT:
            time.sleep(poll_interval)
        for event in event_filter.get_new_entries():
            print("\nНовый лот")
            print(f"id лота: {event['args']['lotId']}")
            print(f"Продавец: {event['args']['owner']}")
            print(f"Адрес токена: {event['args']['tokenAddress']}")
            print(f"Цена за 1 единицу: {event['args']['price']}")
            print(f"Количество единиц: {event['args']['amount']}")
        time.sleep(poll_interval)


def log_loop_cancel(event_filter, poll_interval):
    while True:
        while not PRINT_EVENT:
            time.sleep(poll_interval)
        for event in event_filter.get_new_entries():
            print("\nОтмена продажи")
            print(f"id лота: {event['args']['lotId']}")
            print(f"Количество единиц снятых с продажи: {event['args']['amount']}")
        time.sleep(poll_interval)


def log_loop_change_price(event_filter, poll_interval):
    while True:
        while not PRINT_EVENT:
            time.sleep(poll_interval)
        for event in event_filter.get_new_entries():
            print("\nИзменена цена")
            print(f"id лота: {event['args']['lotId']}")
            print(f"Старая цена: {event['args']['oldPrice']}")
            print(f"Новая цена: {event['args']['newPrice']}")
        time.sleep(poll_interval)


def log_loop_purchase(event_filter, poll_interval):
    while True:
        while not PRINT_EVENT:
            time.sleep(poll_interval)
        for event in event_filter.get_new_entries():
            print("\nНовый лот")
            print(f"id лота: {event['args']['lotId']}")
            print(f"Адрес токена: {event['args']['tokenAddress']}")
            print(f"Цена за 1 единицу: {event['args']['price']}")
            print(f"Куплено единиц: {event['args']['amount']}")
            print(f"Покупатель: {event['args']['customer']}")
        time.sleep(poll_interval)


event_filter_list_lot = MARKETPLACE.events.AddProposal.create_filter(fromBlock="latest")
event_filter_cancel = MARKETPLACE.events.FinishProposal.create_filter(fromBlock="latest")
event_filter_change_price = MARKETPLACE.events.Transfer.create_filter(fromBlock="latest")
event_filter_purchase = MARKETPLACE.events.Approval.create_filter(fromBlock="latest")
