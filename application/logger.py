import datetime


def add_log(info):
    """
    Функция для добавления записи в лог-файл.

    :param info: Информация, которую нужно добавить в лог.
    :type info: str
    """
    log = str(datetime.datetime.now()) + '\n' + info + '\n' # Формирует строку лога с датой и временем
    with open('logs.log', 'a', encoding='utf8') as fl: # Открывает файл logs.log в режиме добавления
        fl.write(log) # Записывает строку лога в файл
