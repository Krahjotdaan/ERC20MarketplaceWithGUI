import time
from threading import Thread
from application.keys import MARKETPLACE, get_application, get_wallet
from application.marketplace_functions import lot_id, lot_info
from application.logger import *


def log_loop_list_lot(event_filter, poll_interval):
    """
    Функция, которая непрерывно отслеживает события ListLot в блокчейне и обновляет UI.

    :param event_filter: Фильтр событий, используемый для получения событий ListLot.
    :type event_filter: MARKETPLACE.events.ListLot.Filter
    :param poll_interval: Интервал в секундах, с которым проверяются новые события.
    :type poll_interval: float
    """
    application = get_application()
    while True:
        
        try:
            for event in event_filter.get_new_entries():
                """
                Обрабатывает каждое новое событие ListLot.

                :param event: Событие ListLot.
                :type event: dict
                """
                event_info = f"Новый лот\nid лота: {event['args']['lotId']}\nПродавец: {event['args']['owner']}\nАдрес токена: {event['args']['tokenAddress']}\nНазвание: {event['args']['name']}\nСимвол: {event['args']['symbol']}\nДесятичных токенов: {event['args']['decimals']}\nЦена за 1 единицу: {event['args']['price']} wei\nКоличество единиц: {event['args']['amount']}\n"
                application.ui.events_display.append(event_info) # Добавляет информацию о событии в UI
                id = int(event['args']['lotId']) # Получает ID лота из события
                lot = lot_info(id) # Получает информацию о лоте по ID
                application.lots[str(id)] = lot # Сохраняет информацию о лоте в приложении
                application.create_lot_widget(id, lot) # Создает виджет лота в UI
                application.ui.last_id.setText(f"Id последнего лота: {lot_id()}") # Обновляет ID последнего лота
                add_log(event_info) # Добавляет информацию о событии в лог
            time.sleep(poll_interval) # Ожидает указанный интервал
        except ValueError:
            """
            Обрабатывает исключение ValueError, которое может возникнуть при обработке событий.

            Это происходит, когда срок действия фильтра событий истек. В этом случае создается новый фильтр,
            который начинается с последнего блока.
            """
            event_filter = MARKETPLACE.events.ListLot.create_filter(fromBlock="latest")


def log_loop_cancel(event_filter, poll_interval):
    """
    Функция, которая непрерывно отслеживает события Cancel в блокчейне и обновляет UI.

    :param event_filter: Фильтр событий, используемый для получения событий Cancel.
    :type event_filter: MARKETPLACE.events.Cancel.Filter
    :param poll_interval: Интервал в секундах, с которым проверяются новые события.
    :type poll_interval: float
    """
    application = get_application()
    while True:
        try:
            for event in event_filter.get_new_entries():
                """
                Обрабатывает каждое новое событие Cancel.

                :param event: Событие Cancel.
                :type event: dict
                """
                event_info = f"Отмена продажи\nid лота: {event['args']['lotId']}\nКоличество единиц снятых с продажи: {event['args']['amount']}\n"
                application.ui.events_display.append(event_info) # Добавляет информацию о событии в UI
                id = str(event['args']['lotId']) # Получает ID лота из события
                application.lots[id][3] -= int(event['args']['amount']) # Уменьшает количество токенов в лоте на amount

                if application.lots[id][3] == 0: # Если количество токенов равно 0, то из UI удаляется соответствующий виджет
                    application.ui.events_display.append("Лот полностью снят с продажи\n")
                    add_log(event_info + "Лот полностью снят с продажи\n") # Добавляет информацию о событии в лог

                    # Удаление виджета из UI
                    row = application.ui.list_all_lots.indexFromItem(application.lot_widgets[id]).row()
                    item = application.ui.list_all_lots.takeItem(row)
                    application.ui.list_all_lots.removeItemWidget(item)
                    application.ui.list_all_lots.update()

                    if application.lots[id][0] == get_wallet(): # Если владельцем снятого с продажи лота является пользователь, то виджет удаляется из вкладки Мои лоты
                        # Удаление виджета из UI
                        row1 = application.ui.list_my_lots.indexFromItem(application.my_lots_widgets[id]).row()
                        item1 = application.ui.list_my_lots.takeItem(row1)
                        application.ui.list_my_lots.removeItemWidget(item1)
                        application.ui.list_my_lots.update()
                    del application.lots[id]

                else: # Если снята с продажи только часть токенов, то обновляется соответствующий виджет
                    add_log(event_info) # Добавляет информацию о событии в лог

                    #Обновление виджета в UI
                    row = application.ui.list_all_lots.indexFromItem(application.lot_widgets[id]).row()
                    lot = application.lots[id]
                    application.ui.list_all_lots.item(row).setText(f"id: {id}\nПродавец: {lot[0]}\nАдрес токена: {lot[1]}\nНазвание: {lot[4]}\nСимвол: {lot[5]}\nДесятичных токенов: {lot[6]}\nЦена за 1 единицу: {lot[2]} wei\nКоличество единиц: {lot[3]}\n")
                    application.ui.list_all_lots.update()

                    if application.lots[id][0] == get_wallet(): # Если владельцем лота является пользователь, то обновляется соответствующий виджет во вкладке Мои лоты
                        #Обновление виджета в UI
                        row1 = application.ui.list_my_lots.indexFromItem(application.my_lots_widgets[id]).row()
                        application.ui.list_my_lots.item(row1).setText(f"id: {id}\nПродавец: {lot[0]}\nАдрес токена: {lot[1]}\nНазвание: {lot[4]}\nСимвол: {lot[5]}\nДесятичных токенов: {lot[6]}\nЦена за 1 единицу: {lot[2]} wei\nКоличество единиц: {lot[3]}\n")
                        application.ui.list_my_lots.update()

            time.sleep(poll_interval) # Ожидает указанный интервал
        except ValueError:
            """
            Обрабатывает исключение ValueError, которое может возникнуть при обработке событий.

            Это происходит, когда срок действия фильтра событий истек. В этом случае создается новый фильтр,
            который начинается с последнего блока.
            """
            event_filter = MARKETPLACE.events.Cancel.create_filter(fromBlock="latest")


def log_loop_change_price(event_filter, poll_interval):
    """
    Функция, которая непрерывно отслеживает события ChangePrice в блокчейне и обновляет UI.

    :param event_filter: Фильтр событий, используемый для получения событий ChangePrice.
    :type event_filter: MARKETPLACE.events.ChangePrice.Filter
    :param poll_interval: Интервал в секундах, с которым проверяются новые события.
    :type poll_interval: float
    """
    application = get_application()
    while True:
        try:
            for event in event_filter.get_new_entries():
                """
                Обрабатывает каждое новое событие ChangePrice.

                :param event: Событие ChangePrice.
                :type event: dict
                """
                event_info = f"Изменена цена\nid лота: {event['args']['lotId']}\nСтарая цена: {event['args']['oldPrice']} wei\nНовая цена: {event['args']['newPrice']} wei\n"
                application.ui.events_display.append(event_info) # Добавляет информацию о событии в UI
                add_log(event_info) # Добавляет информацию о событии в лог
                id = str(event['args']['lotId']) # Получает ID лота из события
                application.lots[id][2] = int(event['args']['newPrice']) # В информации о лоте изменяется цена
                
                #Обновление виджета в UI
                row = application.ui.list_all_lots.indexFromItem(application.lot_widgets[id]).row()
                lot = application.lots[id]
                application.ui.list_all_lots.item(row).setText(f"id: {id}\nПродавец: {lot[0]}\nАдрес токена: {lot[1]}\nНазвание: {lot[4]}\nСимвол: {lot[5]}\nДесятичных токенов: {lot[6]}\nЦена за 1 единицу: {lot[2]} wei\nКоличество единиц: {lot[3]}\n")
                application.ui.list_all_lots.update()

                if application.lots[id][0] == get_wallet(): # Если владельцем лота является пользователь, то обновляется соответствующий виджет во вкладке Мои лоты
                    #Обновление виджета в UI
                    row1 = application.ui.list_my_lots.indexFromItem(application.my_lots_widgets[id]).row()
                    application.ui.list_my_lots.item(row1).setText(f"id: {id}\nПродавец: {lot[0]}\nАдрес токена: {lot[1]}\nНазвание: {lot[4]}\nСимвол: {lot[5]}\nДесятичных токенов: {lot[6]}\nЦена за 1 единицу: {lot[2]} wei\nКоличество единиц: {lot[3]}\n")
                    application.ui.list_my_lots.update()

            time.sleep(poll_interval) # Ожидает указанный интервал
        except ValueError:
            """
            Обрабатывает исключение ValueError, которое может возникнуть при обработке событий.

            Это происходит, когда срок действия фильтра событий истек. В этом случае создается новый фильтр,
            который начинается с последнего блока.
            """
            event_filter = MARKETPLACE.events.ChangePrice.create_filter(fromBlock="latest")


def log_loop_purchase(event_filter, poll_interval):
    """
    Функция, которая непрерывно отслеживает события Purchase в блокчейне и обновляет UI.

    :param event_filter: Фильтр событий, используемый для получения событий Purchase.
    :type event_filter: MARKETPLACE.events.Purchase.Filter
    :param poll_interval: Интервал в секундах, с которым проверяются новые события.
    :type poll_interval: float
    """
    application = get_application()
    while True:
        try:
            for event in event_filter.get_new_entries():
                """
                Обрабатывает каждое новое событие Purchase.

                :param event: Событие Purchase.
                :type event: dict
                """
                event_info = f"Покупка\nid лота: {event['args']['lotId']}\nАдрес токена: {event['args']['tokenAddress']}\nЦена за 1 единицу: {event['args']['price']} wei\nКуплено единиц: {event['args']['amount']}\nПокупатель: {event['args']['customer']}\n"
                application.ui.events_display.append(event_info) # Добавляет информацию о событии в UI
                id = str(event['args']['lotId']) # Получает ID лота из события
                application.lots[id][3] -= int(event['args']['amount']) # Уменьшает количество токенов в лоте на количество купленых токенов

                if application.lots[id][3] == 0: # Если количество токенов равно 0, то из UI удаляется соответствующий виджет
                    application.ui.events_display.append("Лот выкуплен\n")
                    add_log(event_info + "Лот выкуплен\n") # Добавляет информацию о событии в лог
                    # Удаление виджета из UI
                    row = application.ui.list_all_lots.indexFromItem(application.lot_widgets[id]).row()
                    item = application.ui.list_all_lots.takeItem(row)
                    application.ui.list_all_lots.removeItemWidget(item)
                    application.ui.list_all_lots.update()

                    if application.lots[id][0] == get_wallet(): # Если владельцем выкупленного лота является пользователь, то виджет удаляется из вкладки Мои лоты
                        #Удаление виджета из UI
                        row1 = application.ui.list_my_lots.indexFromItem(application.my_lots_widgets[id]).row()
                        item1 = application.ui.list_my_lots.takeItem(row1)
                        application.ui.list_my_lots.removeItemWidget(item1)
                        application.ui.list_my_lots.update()
                    del application.lots[id]

                else: # Если куплена только часть токенов лота, то обновляется соответствующий виджет
                    add_log(event_info) # Добавляет информацию о событии в лог
                    # Обновление виджета в UI
                    row = application.ui.list_all_lots.indexFromItem(application.lot_widgets[id]).row()
                    lot = application.lots[id]
                    application.ui.list_all_lots.item(row).setText(f"id: {id}\nПродавец: {lot[0]}\nАдрес токена: {lot[1]}\nНазвание: {lot[4]}\nСимвол: {lot[5]}\nДесятичных токенов: {lot[6]}\nЦена за 1 единицу: {lot[2]} wei\nКоличество единиц: {lot[3]}\n")
                    application.ui.list_all_lots.update()

                    if application.lots[id][0] == get_wallet(): # Если владельцем лота является пользователь, то обновляется соответствующий виджет во вкладке Мои лоты
                        # Обновление виджета в UI
                        row1 = application.ui.list_my_lots.indexFromItem(application.my_lots_widgets[id]).row()
                        application.ui.list_my_lots.item(row1).setText(f"id: {id}\nПродавец: {lot[0]}\nАдрес токена: {lot[1]}\nНазвание: {lot[4]}\nСимвол: {lot[5]}\nДесятичных токенов: {lot[6]}\nЦена за 1 единицу: {lot[2]} wei\nКоличество единиц: {lot[3]}\n")
                        application.ui.list_my_lots.update()
            time.sleep(poll_interval) # Ожидает указанный интервал
        except ValueError:
            """
            Обрабатывает исключение ValueError, которое может возникнуть при обработке событий.

            Это происходит, когда срок действия фильтра событий истек. В этом случае создается новый фильтр,
            который начинается с последнего блока.
            """
            event_filter = MARKETPLACE.events.Purchase.create_filter(fromBlock="latest")


# Создание фильтров для каждого события
event_filter_list_lot = MARKETPLACE.events.ListLot.create_filter(fromBlock="latest")
event_filter_cancel = MARKETPLACE.events.Cancel.create_filter(fromBlock="latest")
event_filter_change_price = MARKETPLACE.events.ChangePrice.create_filter(fromBlock="latest")
event_filter_purchase = MARKETPLACE.events.Purchase.create_filter(fromBlock="latest")

# Создание потоков для отслеживания событий
thread_list_lot = Thread(target=log_loop_list_lot, args=(event_filter_list_lot, 3))
thread_cancel = Thread(target=log_loop_cancel, args=(event_filter_cancel, 3))
thread_change_price = Thread(target=log_loop_change_price, args=(event_filter_change_price, 3))
thread_purchase = Thread(target=log_loop_purchase, args=(event_filter_purchase, 3))
