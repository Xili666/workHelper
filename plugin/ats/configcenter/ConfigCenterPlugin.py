from logging import Logger

from config.ConfigManager import ConfigManager
import os
import util.WinUtil as WinUtil


class ConfigCenterPlugin(object):
    __doc__ = '''
    ConfigCenter插件
    set key=value 在当前项目设置配置, 在切换项目时会自动保存
    del key 删除配置
    start [projectName] 不使用projectName参数, 启动上次运行的项目
    stop 
    '''

    def __init__(self, config: ConfigManager, logger: Logger):
        self.cc_pid = None
        self.config = config
        self.logger = logger
        self.tomcat_path = self.config.get_config('ats.configCenter.path')
        self.config_path = os.path.join(self.tomcat_path, 'webapps/config-center-server/WEB-INF/classes')

    def project(self, args='default'):
        project_config_file = os.path.join(self.config_path, 'common-config-{}.properties'.format(args[0]))
        if os.path.exists(project_config_file):
            self.logger.warning('使用配置文件{}'.format(project_config_file))
            config_file = os.path.join(self.config_path, 'common-config.properties')
            with open(project_config_file, 'r', encoding='utf-8') as fr:
                with open(config_file, 'w', encoding='utf-8') as fw:
                    for line in fr:
                        fw.write(line)
        else:
            raise OSError('配置文件不存在{}'.format(project_config_file))
        pass

    def start(self, args=None):
        if args:
            self.project(args)
        print('正在启动Config Center')
        self.logger.info('正在启动Config Center')
        os.system('{}: & cd {}/bin & {}/bin/startup.bat'.format(self.tomcat_path.split(':')[0],
                                                                self.tomcat_path, self.tomcat_path))

    def stop(self, args=None):
        print('正在关闭Config Center')
        self.logger.info('正在关闭Config Center')
        WinUtil.kill_commandline(self.tomcat_path)
