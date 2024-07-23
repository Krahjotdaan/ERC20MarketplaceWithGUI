from keys import PRINT_EVENT


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
    pass
