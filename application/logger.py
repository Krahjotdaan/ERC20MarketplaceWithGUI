import datetime


def add_log(info):
    log = str(datetime.datetime.now()) + '\n' + info + '\n'
    with open('logs.log', 'a', encoding='utf8') as fl:
        fl.write(log)
