import os
from logging import Logger

from config.ConfigManager import ConfigManager
from util import WinUtil
import xml.dom.minidom


class UniqueCodePlugin(object):
    __doc__ = '''
    唯一码插件
    start: 启动唯一码服务
    stop: 关闭唯一码服务
    db 修改配置文件数据源配置:
        driverClassName: oracle.jdbc.driver.OracleDriver
        url: url=jdbc:oracle:thin:@127.0.0.1:1521/orcl
        username: username=jats001
        password: password=jats001
         
    '''

    def __init__(self, config: ConfigManager, logger: Logger):
        self.uq_pid = None
        self.uq_home = config.get_config('ats.uniqueCode.path')
        self.uq_data_source = config.get_config('ats.uniqueCode.dataSource')
        self.uq_filename = 'uqServer.cmd'
        self.logger = logger
        pass

    def db(self, args=None):
        for part in args:
            kv = part.spilt('=', 1)
            self.uq_data_source[kv[0]] = kv[1]
        doc = xml.dom.minidom.parse(self.uq_home + '/conf/applicationContext.xml')
        beans = doc.getElementsByTagName('beans')[0]
        bean_list = beans.getElementsByTagName('bean')
        for bean in bean_list:
            if 'dataSource' == bean.getAttribute('id'):
                prop_list = bean.getElementsByTagName('property')
                for prop in prop_list:
                    prop_name = prop.getAttribute('name')
                    if self.uq_data_source.get(prop_name) is not None:
                        prop.setAttribute('value', self.uq_data_source[prop_name])
                break
        pass

    def start(self, args=None):
        proc_id = WinUtil.get_commandline_pid('uniquecode-server')
        if len(proc_id) > 0:
            self.logger.info('唯一码服务启动已经启动')
            print('唯一码服务启动已经启动')
        else:
            self.uq_pid = WinUtil.run_task('uniquecode',
                                           self.uq_home + '/bin/' + self.uq_filename,
                                           WinUtil.log_runnable,
                                           lambda: (self.logger.info('唯一码服务进程被终止'), print('唯一码服务进程被终止')),
                                           self.logger)
            self.logger.info('唯一码服务启动正在启动')
            print('唯一码服务启动正在启动')

    def stop(self, args=None):
        proc_id = WinUtil.get_commandline_pid('uniquecode-server')
        if len(proc_id) > 0:
            command = 'taskkill /F /PID {}'.format(proc_id[0])
            self.logger.warning('执行系统命令 {}'.format(command))
            try:
                os.system(command)
                self.logger.info('唯一码服务进程已结束')
                print('唯一码服务进程已结束')
            except ProcessLookupError as err:
                self.logger.exception(err)
                print('结束唯一码服务进程异常, 没有这个进程')
        else:
            self.logger.info('没有正在运行的唯一码服务')
            print('没有正在运行的唯一码服务')
        if self.uq_pid is not None:
            self.uq_pid.terminate()
            self.uq_pid = None
