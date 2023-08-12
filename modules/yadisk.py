from modules.backup import pack_directory
from datetime import datetime, timedelta
from modules.log import write_log
from hurry.filesize import size
from datetime import datetime
import configparser
import yadisk
import time
import os

config = configparser.ConfigParser()
config.sections()

config.read('config.ini')


def upload_to_yadisk(file_path, destination_path, token):
    try:
        run_yadisk = yadisk.YaDisk(token=token)
        run_yadisk.upload(file_path, destination_path)

        write_log(f'Файл бэкапа: {file_path} загружен на Яндекс.Диск в директорию {destination_path}. ')
    except Exception as ex:
        write_log(ex, 'ERROR')
    finally:
        os.remove(file_path)
        write_log(f'Временный файл: {file_path} УДАЛЕН')


def deleting_old_backups(backup_dir, token):
    run_yadisk = yadisk.YaDisk(token=token)
    current_timestamp = int(time.time())

    for i in list(run_yadisk.listdir(backup_dir)):
        date_to_check = float(str(i['name']).split('_')[-1])
        current_date = datetime.fromtimestamp(current_timestamp)
        period_for_deletion = current_date - timedelta(days=int(config['SETTING']['DAYS_DEL']))

        if datetime.fromtimestamp(date_to_check) > period_for_deletion:
            write_log(f"Архив бэкапа {i['name']} младше {int(config['SETTING']['DAYS_DEL'])} дней.", "PASS")
        else:
            run_yadisk.remove(f"{backup_dir}/{i['name']}", permanently=True)
            write_log(f"Архив бэкапа {i['name']} старше {int(config['SETTING']['DAYS_DEL'])} дней. УДАЛЕН!", "DELETE")


def deleting_max_backups(backup_dir, token):
    run_yadisk = yadisk.YaDisk(token=token)
    list_files = []

    for i in list(run_yadisk.listdir(backup_dir)):
        list_files.append(i['name'])

    print(len(list_files))

    if len(list_files) >= (int(config['SETTING']['MAX_BACKUP']) + 1):
        num_extra_files = len(list_files) - int(config['SETTING']['MAX_BACKUP'])
        files_to_delete = sorted(list_files)[:num_extra_files]
        write_log(f"Общее количество бэкапов {len(list_files)}, максимальное хранимое количество"
                  f" {config['SETTING']['MAX_BACKUP']}.", "DELETE")

        for file_name in files_to_delete:
            run_yadisk.remove(backup_dir + "/" + file_name, permanently=True)
            write_log(f"Бэкап {file_name} удален!", "DELETE")


def information(token):
    run_yadisk = yadisk.YaDisk(token=token)
    ya_info = run_yadisk.get_disk_info()
    remaining_seat = int(int(ya_info['total_space']) - int(ya_info['used_space']))

    write_log(f"Оставшееся место на Яндекс.Диск {remaining_seat} байт ({size(remaining_seat)})", "disk_info")

    if remaining_seat <= 2147483648:
        write_log(f"Мало места! Осталось - {remaining_seat}байт ({size(remaining_seat)})", "disk_info")
    elif remaining_seat <= 1073741824:
        write_log(f"Места осталось менее 1 гигабайта!!!! {remaining_seat}байт ({size(remaining_seat)}). "
                  f"Создание бэкапов остановлено!!!", "disk_info")
        exit(f"Места осталось менее 1 гигабайта!!!! {remaining_seat} байт ({size(remaining_seat)}). "
             "Создание бэкапов остановлено!!!")

    return True


def start():
    yandex_token = config['SETTING']['TOKEN_YADISK']
    source_directory = ("".join((config['SETTING']['PATH_BACKUP_DIR']).split(","))).split()
    backup_dir = config['SETTING']['PATH_TEMP_DIR']
    excluded_directories = ("".join((config['SETTING']['DIR_EXCEPTION']).split(","))).split()

    if information(yandex_token):
        upload_to_yadisk(pack_directory(source_directory, backup_dir, excluded_directories),
                         f"/{config['SETTING']['NAME_BACKUP_DIR_CLOUD']}/"
                         f"{config['SETTING']['NAME_BACKUP']}_"
                         f"{str(int(datetime.timestamp(datetime.now())))}",
                         yandex_token)

        deleting_old_backups(config['SETTING']['NAME_BACKUP_DIR_CLOUD'], yandex_token)
        deleting_max_backups(config['SETTING']['NAME_BACKUP_DIR_CLOUD'], yandex_token)
    else:
        write_log(f"Произошла неизвестная ошибка!", "error")


# https://pypi.org/project/yadisk/
