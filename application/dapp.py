from menu import event_tracking_setup
from event_trackers import thread_list_lot, thread_cancel, thread_change_price, thread_purchase


def main():
    thread_list_lot.start()
    thread_cancel.start()
    thread_change_price.start()
    thread_purchase.start()

    print("\nПриложение работает в тестовой сети Holesky. Чтобы посмотреть подробную информацию о транзакциях, перейдите на https://holesky.etherscan.io/")

    event_tracking_setup()


if __name__ == "__main__":
    main()
    