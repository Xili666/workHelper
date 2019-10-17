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
        self.config = config
        self.container_name = self.config.get_config('ats.redis.docker.containerName')
        self.use_docker = self.config.get_config('ats.redis.docker.useDocker')  # 使用docker
        self.redis_filename = 'redis-server.exe'
        self.logger = logger

    def start_redis(self):
        if WinUtil.get_name_pid(self.redis_filename) is not None:
            self.logger.info('redis进程已经启动')
            print('redis进程已经启动')
        else:
            home_path = self.config.get_config('ats.redis.path')
            self.redis_pid = WinUtil.run_task('redis',
                                              home_path + '/' + self.redis_filename,
                                              WinUtil.log_runnable,
                                              lambda: (self.logger.info('redis进程被终止'), print('redis进程被终止')),
                                              self.logger)
            self.logger.info('redis进程正在启动')
            print('redis进程正在启动')

    def start_docker(self):
        port = self.config.get_config('ats.redis.port')
        docker_cmd = 'docker run --name {} -p {}:6379 -d redis'.format(
            self.container_name, '6379' if not port else str(port))
        out, err = WinUtil.exec_cmd(docker_cmd)  # 启动docker-redis
        if len(out) == 65 and not len(err):
            print('{} 启动成功'.format(self.container_name))
            self.logger.info('{} 启动成功'.format(self.container_name))
        else:
            print('{} 启动失败'.format(self.container_name))
            print(err)
            self.logger.error('{} 启动失败 {}'.format(self.container_name, err))
        pass

    def start(self, args=None):
        if self.use_docker:
            self.start_docker()
        else:
            self.start_redis()
        pass

    def stop_redis(self):
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

    def stop_docker(self):
        out, err = WinUtil.exec_cmd('docker stop {}'.format(self.container_name))
        if out.startswith(self.container_name):
            out, err = WinUtil.exec_cmd('docker rm {}'.format(self.container_name))
            if out.startswith(self.container_name):
                print('{} 关闭成功'.format(self.container_name))
            else:
                print('{} 关闭失败 {}'.format(self.container_name, err))
        else:
            print('{} 关闭失败 {}'.format(self.container_name, err))
        pass

    def stop(self, args=None):
        if self.use_docker:
            self.stop_docker()
        else:
            self.stop_redis()

    def rdb(self, args=None):
        if self.use_docker:
            pass
        else:
            if type(args) is list and len(args) < 1:
                print('redis rdb 缺少必要的参数')
            else:
                rdb_path = 'dump.rdb'
                if os.path.exists(rdb_path):
                    self.logger.warning('删除文件: {}'.format(rdb_path))
                    os.remove(rdb_path)
                    self.logger.info('已删除文件:{}'.format(rdb_path))
                    print('已删除文件:{}'.format(rdb_path))
