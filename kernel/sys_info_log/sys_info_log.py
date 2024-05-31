import psutil
import time
import logging
import logging.handlers
from multiprocessing import Process
import json

def get_cpu_info():
    cpu_percent = psutil.cpu_percent()
    cpu_count = psutil.cpu_count()
    cpu_stats = psutil.cpu_stats()
    cpu_times = psutil.cpu_times()

    # CPU Info Json Type Data
    cpu_data = {
        "cpu_usage": cpu_percent,
        "cpu_count" : cpu_count,
        "cpu_times" : {},
        "cpu_stats" : {}
    }

    # add cpu_times in cpu_data
    for i in range(len(cpu_times)):
        cpu_data["cpu_times"][cpu_times._fields[i]] = cpu_times[i]

    # add cpu_stats in cpu_data
    for i in range(len(cpu_stats)):
        cpu_data["cpu_stats"][cpu_stats._fields[i]] = cpu_stats[i]

    cpu_data = json.dumps(cpu_data)

    logger = logging.getLogger('cpu')
    logger.setLevel(logging.INFO)

    #add handler to the logger
    handler = logging.FileHandler('/var/log/sys_info')

    #add formatter to the handler
    formatter = logging.Formatter('[%(asctime)s - %(name)s - %(levelname)s] %(message)s') # [로그발생시간 - 로그레벨] 로그 메세지

    handler.formatter = formatter
    logger.addHandler(handler)
    logger.info(cpu_data)

def get_memory_info():
    memory = psutil.virtual_memory()
    used_memory = memory.used / (1024 * 1024) # 메모리 사용량을 MB 단위로 변환
    available_memory = memory.available / (1024 * 1024) # 사용 가능한 메모리 양을 MB 단위로 변환
    swap_memory = psutil.swap_memory()
    
    memory_data = {
        "used_memory" : used_memory,
        "available_memory" : available_memory,
        "swap_memory" : {}
    }

    for i in range(len(swap_memory)):
        memory_data["swap_memory"][swap_memory._fields[i]] = swap_memory[i]

    memory_data = json.dumps(memory_data)

    logger = logging.getLogger('memory')
    logger.setLevel(logging.INFO)

    #add handler to the logger
    handler = logging.FileHandler('/var/log/sys_info')

    #add formatter to the handler
    formatter = logging.Formatter('[%(asctime)s - %(name)s - %(levelname)s] %(message)s') # [로그발생시간 - 로그레벨] 로그 메세지

    handler.formatter = formatter
    logger.addHandler(handler)
    logger.info(memory_data)

if __name__ == '__main__':
    while True:
        get_cpu_info()
        get_memory_info()
        time.sleep(2)
