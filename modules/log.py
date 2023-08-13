import os
from datetime import datetime


def write_log(text, level='INFO', log_save_directory=os.path.dirname(os.path.abspath(__file__))):
    with open(f'{log_save_directory}/logs/program_logs.txt', 'a') as log:
        log.write(f"[{str(int(datetime.timestamp(datetime.now())))}]*[{level.upper()}] >> {text}\n")
