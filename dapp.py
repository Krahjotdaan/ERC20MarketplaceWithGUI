from application.menu import event_tracking_setup
from application.event_threads import *


def main():
    thread_list_lot.start()
    thread_cancel.start()
    thread_change_price.start()
    thread_purchase.start()
    
    print("\nПриложение работает в тестовой сети Sepolia. Чтобы посмотреть подробную информацию о транзакциях, перейдите на https://sepolia.etherscan.io/")

    event_tracking_setup()


if __name__ == "__main__":
    main()
    