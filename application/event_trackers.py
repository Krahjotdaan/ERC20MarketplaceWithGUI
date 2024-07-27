import time
from threading import Thread
from application.keys import MARKETPLACE, get_application
from application.marketplace_functions import lot_info


def log_loop_list_lot(event_filter, poll_interval):
    application = get_application()
    while True:
        try:
            for event in event_filter.get_new_entries():
                application.ui.events_display.append(
                    f"Новый лот\nid лота: {event['args']['lotId']}\nПродавец: {event['args']['owner']}\nАдрес токена: {event['args']['tokenAddress']}\nНазвание: {event['args']['name']}\nСимвол: {event['args']['symbol']}\nДесятичных токенов: {event['args']['decimals']}\nЦена за 1 единицу: {event['args']['price']} wei\nКоличество единиц: {event['args']['amount']}\n"
                )
                id = int(event['args']['lotId'])
                lot = lot_info(id)
                application.lots[str(id)] = lot
                application.create_lot_widget(id, lot)
            time.sleep(poll_interval)
        except ValueError:
            event_filter = MARKETPLACE.events.ListLot.create_filter(fromBlock="latest")


def log_loop_cancel(event_filter, poll_interval):
    application = get_application()
    while True:
        try:
            for event in event_filter.get_new_entries():
                application.ui.events_display.append(
                    f"Отмена продажи\nid лота: {event['args']['lotId']}\nКоличество единиц снятых с продажи: {event['args']['amount']}\n"
                )
                application.lots[str(event['args']['lotId'])][3] -= int(event['args']['amount'])
                if application.lots[str(event['args']['lotId'])][3] == 0:
                    row = application.ui.list_all_lots.indexFromItem(application.lot_widgets[str(event['args']['lotId'])]).row()
                    item = application.ui.list_all_lots.takeItem(row)
                    application.ui.list_all_lots.removeItemWidget(item)
                    application.ui.list_all_lots.update()
                else:
                    row = application.ui.list_all_lots.indexFromItem(application.lot_widgets[str(event['args']['lotId'])]).row()
                    lot = application.lots[str(event['args']['lotId'])]
                    application.ui.list_all_lots.item(row).setText(f"id: {str(event['args']['lotId'])}\nПродавец: {lot[0]}\nАдрес токена: {lot[1]}\nНазвание: {lot[4]}\nСимвол: {lot[5]}\nДесятичных токенов: {lot[6]}\nЦена за 1 единицу: {lot[2]} wei\nКоличество единиц: {lot[3]}\n")
                    application.ui.list_all_lots.update()

            time.sleep(poll_interval)
        except ValueError:
            event_filter = MARKETPLACE.events.Cancel.create_filter(fromBlock="latest")


def log_loop_change_price(event_filter, poll_interval):
    application = get_application()
    while True:
        try:
            for event in event_filter.get_new_entries():
                application.ui.events_display.append(
                    f"Изменена цена\nid лота: {event['args']['lotId']}\nСтарая цена: {event['args']['oldPrice']} wei\nНовая цена: {event['args']['newPrice']} wei\n"
                )
                application.lots[str(event['args']['lotId'])][2] = int(event['args']['newPrice'])
                row = application.ui.list_all_lots.indexFromItem(application.lot_widgets[str(event['args']['lotId'])]).row()
                lot = application.lots[str(event['args']['lotId'])]
                application.ui.list_all_lots.item(row).setText(f"id: {str(event['args']['lotId'])}\nПродавец: {lot[0]}\nАдрес токена: {lot[1]}\nНазвание: {lot[4]}\nСимвол: {lot[5]}\nДесятичных токенов: {lot[6]}\nЦена за 1 единицу: {lot[2]} wei\nКоличество единиц: {lot[3]}\n")
                application.ui.list_all_lots.update()
            time.sleep(poll_interval)
        except ValueError:
            event_filter = MARKETPLACE.events.ChangePrice.create_filter(fromBlock="latest")


def log_loop_purchase(event_filter, poll_interval):
    application = get_application()
    while True:
        try:
            for event in event_filter.get_new_entries():
                application.ui.events_display.append(
                    f"Покупка\nid лота: {event['args']['lotId']}\nАдрес токена: {event['args']['tokenAddress']}\nЦена за 1 единицу: {event['args']['price']} wei\nКуплено единиц: {event['args']['amount']}\nПокупатель: {event['args']['customer']}\n"
                )
                application.lots[str(event['args']['lotId'])][3] -= int(event['args']['amount'])
                if application.lots[str(event['args']['lotId'])][3] == 0:
                    row = application.ui.list_all_lots.indexFromItem(application.lot_widgets[str(event['args']['lotId'])]).row()
                    item = application.ui.list_all_lots.takeItem(row)
                    application.ui.list_all_lots.removeItemWidget(item)
                    application.ui.list_all_lots.update()
                else:
                    row = application.ui.list_all_lots.indexFromItem(application.lot_widgets[str(event['args']['lotId'])]).row()
                    lot = application.lots[str(event['args']['lotId'])]
                    application.ui.list_all_lots.item(row).setText(f"id: {str(event['args']['lotId'])}\nПродавец: {lot[0]}\nАдрес токена: {lot[1]}\nНазвание: {lot[4]}\nСимвол: {lot[5]}\nДесятичных токенов: {lot[6]}\nЦена за 1 единицу: {lot[2]} wei\nКоличество единиц: {lot[3]}\n")
                    application.ui.list_all_lots.update()
            time.sleep(poll_interval)
        except ValueError:
            event_filter = MARKETPLACE.events.Purchase.create_filter(fromBlock="latest")


event_filter_list_lot = MARKETPLACE.events.ListLot.create_filter(fromBlock="latest")
event_filter_cancel = MARKETPLACE.events.Cancel.create_filter(fromBlock="latest")
event_filter_change_price = MARKETPLACE.events.ChangePrice.create_filter(fromBlock="latest")
event_filter_purchase = MARKETPLACE.events.Purchase.create_filter(fromBlock="latest")

thread_list_lot = Thread(target=log_loop_list_lot, args=(event_filter_list_lot, 3))
thread_cancel = Thread(target=log_loop_cancel, args=(event_filter_cancel, 3))
thread_change_price = Thread(target=log_loop_change_price, args=(event_filter_change_price, 3))
thread_purchase = Thread(target=log_loop_purchase, args=(event_filter_purchase, 3))
