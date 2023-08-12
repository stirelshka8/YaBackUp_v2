import os
from sys import platform
from modules.yadisk import start
from modules.log import write_log


if __name__ == '__main__':

    if platform == "linux" or platform == "linux2":
        if os.geteuid() != 0:
            write_log('Отмена запуска. Пользователь не обладает правами суперпользователя!')
            exit(f"-----------------------------------------------------------------\n"
                 f"Данную программу необходимо запускат с правами суперпользователя!\n"
                 f"-----------------------------------------------------------------")
        else:
            write_log('----------------------------------------------', 'START')
            write_log('*** Запущен процесс резервного копирования ***', 'START')
            write_log('----------------------------------------------', 'START')
            start()

    elif platform == "darwin":
        exit('В данное время запуск возможен только на операционной системе семейства Linux')
    elif platform == "win32":
        exit('В данное время запуск возможен только на операционной системе семейства Linux')


