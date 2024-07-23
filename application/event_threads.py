from threading import Thread
from application.event_trackers import *


thread_list_lot = Thread(target=log_loop_list_lot, args=(event_filter_list_lot, 10))
thread_cancel = Thread(target=log_loop_cancel, args=(event_filter_cancel, 10))
thread_change_price = Thread(target=log_loop_change_price, args=(event_filter_change_price, 10))
thread_purchase = Thread(target=log_loop_purchase, args=(event_filter_purchase, 10))
