import logging
import subprocess


class ProcessHandler(object):
    __singleton = None

    def __new__(cls, *args, **kwargs):
        if not cls.__singleton:
            cls.__singleton = object.__new__(cls)
        return cls.__singleton

    def __init__(self):
        self.logger = logging.getLogger('processHandler')
        self.handler = dict()

    def put_process(self, key: str, process: subprocess.Popen):
        self.logger.info('添加进程{}句柄'.format(key))
        self.handler[key] = process

    @staticmethod
    def get_process_handler():
        return ProcessHandler.__singleton
