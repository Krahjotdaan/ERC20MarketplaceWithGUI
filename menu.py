from keys import PRINT_EVENT
from marketplace_functions import *


def event_tracking_setup():
    global PRINT_EVENT
    print("1. Выводить сообщения о новых событиях")
    print("2. НЕ выводить сообщения о новых событиях")

    try:
        choice = int(input("\nВведите номер пункта меню, который выбрали: "))
    except ValueError:
        choice = int(input("\nВведите номер пункта меню, который выбрали: "))

    if choice == 1:
        PRINT_EVENT = True
    elif choice == 2:
        PRINT_EVENT = False
    else:
        event_tracking_setup()
    menu()


def menu():
    while True:
        print("\nКонтракт Marketplace")
        print("1. Вызвать функцию lot_id")
        print("2. Вызвать функцию lot_info")
        print("3. Вызвать функцию list_lot")
        print("4. Вызвать функцию cancel")
        print("5. Вызвать функцию change_price")
        print("6. Вызвать функцию purchase")
        print("7. Настроить отслеживание событий")
        print("8. Выйти из программы")
        
        try:
            choice = int(input("\nВведите номер пункта меню, который выбрали: "))
        except ValueError:
            choice = int(input("\nВведите номер пункта меню, который выбрали: "))

        if choice == 1:
            lot_id()
        if choice == 2:
            lot_info()
        if choice == 3:
            list_lot()
        if choice == 4:
            cancel()
        if choice == 5:
            change_price()
        if choice == 6:
            purchase()
        if choice == 7:
            event_tracking_setup()
        if choice == 8:
            exit()
        else:
            menu()
