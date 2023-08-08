import os
import tarfile
from datetime import datetime


def pack_directory(source_dirs, destination_dir='/tmp', excluded_dirs=None):
    if excluded_dirs is None:
        excluded_dirs = []

    timestamp = str(int(datetime.timestamp(datetime.now())))
    tar_filename = os.path.join(destination_dir, f'archive_{timestamp}.tar')

    with tarfile.open(tar_filename, 'w') as tar:
        for source_dir in source_dirs:
            for root, dirs, files in os.walk(source_dir):

                dirs[:] = [d for d in dirs if d not in excluded_dirs]

                for file in files:
                    file_path = os.path.join(root, file)

                    if os.access(file_path, os.R_OK):
                        rel_path = os.path.relpath(file_path, source_dir)
                        tar.add(file_path, arcname=os.path.join(os.path.basename(source_dir), rel_path))
                    else:
                        with open('log.txt', 'a') as log:
                            log.write(f"[{timestamp}] >> Пропуск нечитаемого файла: {file_path}\n")
    return tar_filename


def stert():
    # Пример вызова функции
    source_directory = ['/etc', '/usr/bin', '/usr/sbin', '/var/www']
    destination_directory = '/mnt/work'  # Замените на свой путь к целевой директории
    excluded_directories = ['games', 'share']  # Замените на список директорий, которые нужно исключить

    print(pack_directory(source_directory, destination_directory, excluded_directories))
