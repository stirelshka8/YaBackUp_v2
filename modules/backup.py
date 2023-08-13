import os
import tarfile
from datetime import datetime
from modules.log import write_log


def pack_directory(source_dirs,
                   destination_dir=f'{os.path.dirname(os.path.abspath(__file__))}/tmp',
                   excluded_dirs=None):
    write_log(f'Процесс создания временного архива запущен! '
              f'Упаковывается - {source_dirs}. '
              f'Временное расположение архива - {destination_dir}. '
              f'Пропускается - {excluded_dirs}')

    if excluded_dirs is None:
        excluded_dirs = []

    # Формировние имени временного файла и добавление к нему времени в формате TIMESTAMP.
    tar_filename = os.path.join(destination_dir, f'TEMPBACKUP_{str(int(datetime.timestamp(datetime.now())))}')

    with tarfile.open(tar_filename, 'w') as tar:
        for source_dir in source_dirs:
            for root, dirs, files in os.walk(source_dir):

                # Данный код на Python представляет собой генератор списков (list comprehension).
                # Эта строка кода фильтрует список "dirs", удаляя элементы, которые находятся в списке "excluded_dirs".
                dirs[:] = [d for d in dirs if d not in excluded_dirs]

                for file in files:
                    file_path = os.path.join(root, file)

                    # Проверка читаемости файла и добавление в архив.
                    if os.access(file_path, os.R_OK):
                        rel_path = os.path.relpath(file_path, source_dir)
                        tar.add(file_path, arcname=os.path.join(os.path.basename(source_dir), rel_path))
                    else:
                        write_log(f'Пропуск нечитаемого файла: {file_path}', 'PASS')

    write_log(f'Создан временный файл: {tar_filename}')

    return tar_filename
