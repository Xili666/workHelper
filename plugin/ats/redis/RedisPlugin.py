from logging import Logger

from config.ConfigManager import ConfigManager
import os
import util.WinUtil as WinUtil


class RedisPlugin(object):
    __doc__ = '''
    Redis插件
    start: 启动redis
    stop: 关闭redis
    rdb remove: 清除缓存文件
    '''

    def __init__(self, config: ConfigManager, logger: Logger):
        self.redis_pid = None
        self.redis_filename = 'redis-server.exe'
        self.home_path = config.get_config('ats.redis.path')
        self.logger = logger
        pass

    def start(self, args=None):
        if WinUtil.get_name_pid(self.redis_filename) is not None:
            self.logger.info('redis进程已经启动')
            print('redis进程已经启动')
        else:
            self.redis_pid = WinUtil.run_task('redis',
                                              self.home_path + '/' + self.redis_filename,
                                              WinUtil.log_runnable,
                                              lambda: (self.logger.info('redis进程被终止'), print('redis进程被终止')),
                                              self.logger)
            self.logger.info('redis进程正在启动')
            print('redis进程正在启动')

    def stop(self, args=None):
        if self.redis_pid is not None:
            self.redis_pid.terminate()
            self.logger.info('结束redis_pid')
            self.redis_pid = None
            print('redis进程已结束')
        else:
            if WinUtil.get_name_pid(self.redis_filename) is not None:
                command = 'taskkill /F /IM {}'.format(self.redis_filename)
                self.logger.warning('执行系统命令 {}'.format(command))
                try:
                    os.system(command)
                    self.logger.info('redis进程已结束')
                    print('redis进程已结束')
                except ProcessLookupError as err:
                    self.logger.exception(err)
                    print('结束redis进程异常, 没有这个进程')
            else:
                self.logger.info('没有启动的redis进程')
                print('没有启动的redis进程')

    def rdb(self, args=None):
        if type(args) is list and len(args) < 1:
            print('redis rdb 缺少必要的参数')
        else:
            rdb_path = 'dump.rdb'
            if os.path.exists(rdb_path):
                self.logger.warning('删除文件: {}'.format(rdb_path))
                os.remove(rdb_path)
                self.logger.info('已删除文件:{}'.format(rdb_path))
                print('已删除文件:{}'.format(rdb_path))
