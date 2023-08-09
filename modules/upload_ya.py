from modules.backup import pack_directory
from datetime import datetime
import configparser
import yadisk
import os

config = configparser.ConfigParser()
config.sections()

config.read('config.ini')


def upload_to_yadisk(file_path, destination_path, token):
    try:
        run_yadisk = yadisk.YaDisk(token=token)
        run_yadisk.upload(file_path, destination_path)

        with open('log.txt', 'a') as log:
            log.write(f"[{str(int(datetime.timestamp(datetime.now())))}] >> Бэкап загружен на Яндекс.Диск "
                      f"({destination_path}) \n")
    except Exception as ex:
        with open('log.txt', 'a') as log:
            log.write(f"[{str(int(datetime.timestamp(datetime.now())))}] >> ERROR: {ex}\n")
    finally:
        with open('log.txt', 'a') as log:
            log.write(f"[{str(int(datetime.timestamp(datetime.now())))}] >> Временный файл {file_path} УДАЛЕН \n")
        os.remove(file_path)


def start():
    yandex_token = config['SETTING']['TOKEN_YADISK']
    source_directory = ("".join((config['SETTING']['PATH_BACKUP_DIR']).split(","))).split()
    backup_dir = config['SETTING']['PATH_TEMP_DIR']
    excluded_directories = ("".join((config['SETTING']['DIR_EXCEPTION']).split(","))).split()

    upload_to_yadisk(pack_directory(source_directory, backup_dir, excluded_directories),
                     f"/{config['SETTING']['NAME_BACKUP_DIR_CLOUD']}/"
                     f"{config['SETTING']['NAME_BACKUP']}_"
                     f"{str(int(datetime.timestamp(datetime.now())))}"+".tar",
                     yandex_token)

# https://pypi.org/project/yadisk/
