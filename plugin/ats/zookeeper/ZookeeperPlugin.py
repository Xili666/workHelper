import os
from logging import Logger

from config.ConfigManager import ConfigManager
from util import WinUtil, DockerUtil


class ZookeeperPlugin(object):
    __doc__ = '''
        Zookeeper插件
        start [port]: 启动zookeeper
        stop: 关闭zookeeper
        '''

    def __init__(self, config: ConfigManager, logger: Logger):
        self.zk_pid = None
        self.config = config
        self.use_docker = config.get_config('ats.zookeeper.docker.enable')
        self.container_name = self.config.get_config('ats.zookeeper.docker.containerName')
        self.zk_home = config.get_config('ats.zookeeper.path')
        self.zk_port = config.get_config('ats.zookeeper.port')
        self.logger = logger
        pass

    # 修改配置文件的端口
    def __set_zk_port(self):
        with open(self.zk_home + '/conf/zoo.cfg', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        with open(self.zk_home + '/conf/zoo.cfg', 'w', encoding='utf-8') as f:
            for line in lines:
                if line.lstrip().startswith('clientPort'):
                    self.logger.warning('修改zookeeper端口{}, {}'.format(line, self.zk_port))
                    line = 'clientPort={}\n'.format(self.zk_port)
                f.write(line)
        pass

    def start_zk(self, args=None):
        if type(args) is list and len(args) > 0:
            if str(args[0]).isnumeric():
                self.zk_port = args[0]
            else:
                self.logger.info('无效的端口: {}'.format(args[0]))
                print('无效的端口: {}'.format(args[0]))
                return None
        self.__set_zk_port()
        pid = WinUtil.get_port_pid(self.zk_port)
        if pid is None:
            self.zk_pid = WinUtil.run_task('zookeeper',
                                           self.zk_home + '/bin/' + 'zkServer.cmd',
                                           WinUtil.log_runnable,
                                           lambda: (self.logger.info('zookeeper进程被终止'), print('zookeeper进程被终止')),
                                           self.logger)
            self.logger.info('zookeeper进程正在启动')
            print('zookeeper进程正在启动')
        else:
            self.logger.info('端口{}已被进程{}占用'.format(self.zk_port, pid))
            print('端口{}已被进程{}占用'.format(self.zk_port, pid))

    def start_docker(self):
        docker_cmd = 'docker run --name {} -p {}:2181 -d zookeeper'.format(self.container_name, self.zk_port)
        ok, msg = DockerUtil.docker_run(docker_cmd)
        if ok:
            print('{} 启动成功'.format(self.container_name))
            self.logger.info('{} 启动成功'.format(self.container_name))
        else:
            print('{} 启动失败'.format(self.container_name))
            print(msg)
            self.logger.error('{} 启动失败 {}'.format(self.container_name, msg))
        pass

    def start(self, args=None):
        if self.use_docker:
            self.start_docker()
        else:
            self.start_zk(args=args)

    def stop_zk(self, args=None):
        if self.zk_pid is not None:
            self.zk_pid.terminate()
            self.zk_pid = None
            self.logger.info('结束zk_pid')
            print('zookeeper进程已结束')
        else:
            pid = WinUtil.get_port_pid(self.zk_port)
            if pid is not None:
                command = 'taskkill /F /PID {}'.format(pid)
                self.logger.warning('执行系统命令 {}'.format(command))
                try:
                    os.system(command)
                    self.logger.info('zookeeper进程已结束')
                    print('zookeeper进程已结束')
                except ProcessLookupError as err:
                    self.logger.exception(err)
                    print('结束zookeeper进程异常, 没有这个线程')
            else:
                self.logger.info('没有启动的zookeeper进程')
                print('没有启动的zookeeper进程')

    def stop_docker(self):
        out = DockerUtil.docker_stop(self.container_name)
        if out == self.container_name:
            print('{} 关闭成功'.format(self.container_name))
        else:
            print('{} 关闭失败 {}'.format(self.container_name, out))

    def stop(self, args=None):
        if self.use_docker:
            self.stop_docker()
        else:
            self.stop_zk()
