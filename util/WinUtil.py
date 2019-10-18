import os
import subprocess
import threading
import logging
import psutil
import socket

from handler.ProcessHandler import ProcessHandler
from handler.ThreadHandler import ThreadHandler

logger = logging.getLogger('WinUtil')


# 检查指定名称的系统进程是否存在
def get_name_pid(p_name: str):
    for pid in psutil.pids():
        try:
            process = psutil.Process(pid)
        except psutil.NoSuchProcess:
            continue
        if process.name() == p_name:
            return pid
    return None


def get_port_pid(port: int):
    with os.popen('netstat -aon | findstr {}'.format(port)) as p:
        line = p.readline().strip()
        if len(line) > 0:
            return line.split()[-1]
        return None


# 检查端口是否被占用
def is_port_occupied(port: int, host='127.0.0.1'):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
        s.shutdown(2)
        return True
    except OSError:
        return False
    pass


# 根据命令行片段模糊匹配PID
def get_commandline_pid(command: str):
    proc_id = list()
    cmd = "wmic process where \"caption = 'java.exe' and commandline like '%{}%'\" get processId".format(
        command.replace('/', '\\\\'))
    logger.info('执行系统命令: {}'.format(cmd))
    print('执行系统命令: {}'.format(cmd))
    with os.popen(cmd) as o:
        for line in o:
            line = line.strip()
            if len(line) > 0 and line.isnumeric():
                proc_id.append(line)
    return proc_id


# 根据命令行的部分kill
def kill_commandline(command: str):
    for pid in get_commandline_pid(command):
        cmd = 'taskkill /f /pid {}'.format(pid)
        logger.warning('执行系统命令: {}'.format(cmd))
        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, encoding='gbk')
        logger.info(p.stdout)
        logger.error(p.stdout)
    pass


# 通用的日志打印函数, 将在任务执行时调用
def log_runnable(process: subprocess.Popen, task_logger: logging.Logger):
    line = process.stdout.readline()
    if len(line) > 0:
        task_logger.info(str(line, 'gbk').rstrip())


# func: 任务进行中的执行函数
# task_terminate_func: 任务终止时的执行函数
def __runnable(process: subprocess.Popen, name, func, task_terminate_func, logger):
    ThreadHandler.get_thread_handler().put_thread(name, threading.current_thread())
    logger.info("启动线程{} - {}".format(name, threading.current_thread().getName()))
    while process.poll() is None:
        func(process, logger)
    logger.info("线程{}结束运行 {}".format(name, threading.current_thread().getName()))
    ThreadHandler.get_thread_handler().pop_thread(name)
    if task_terminate_func and hasattr(task_terminate_func, '__call__'):
        task_terminate_func()


# 启动一个后台任务
def run_task(name, command, func=log_runnable, task_terminate_func=None, shell=False, logger=logger):
    logger.warning('执行系统命令: {}'.format(command))
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=shell)
    ProcessHandler.get_process_handler().put_process(name, p)  # 将进程统一管理
    thread = threading.Thread(target=__runnable, args=(p, name, func, task_terminate_func, logger))
    thread.setDaemon(True)  # 设置为守护线程, 在应用退出时不会阻塞
    thread.start()
    return p


def exec_cmd(cmd, encoding='gbk'):
    logger.warning('执行系统命令: {}'.format(cmd))
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding=encoding)
    logger.warning(p.stdout)
    logger.error(p.stderr)
    return p.stdout, p.stderr
