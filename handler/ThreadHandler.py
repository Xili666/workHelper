import logging
import threading


class ThreadHandler(object):
    __singleton = None

    def __new__(cls, *args, **kwargs):
        if not cls.__singleton:
            cls.__singleton = object.__new__(cls)
        return cls.__singleton

    def __init__(self):
        self.logger = logging.getLogger('threadHandler')
        self.handler = dict()

    def put_thread(self, key: str, thread: threading):
        if self.handler.get(key) is not None:
            self.logger.error('线程{}已经存在'.format(key))
            raise SyntaxError('线程{}已经存在'.format(key))
        self.logger.info('添加线程{}句柄'.format(key))
        self.handler[key] = thread

    def pop_thread(self, key: str):
        if self.handler.get(key) is not None:
            self.logger.info('线程{}句柄已移除'.format(key))
            return self.handler.pop(key)

    @staticmethod
    def get_thread_handler():
        return ThreadHandler.__singleton
