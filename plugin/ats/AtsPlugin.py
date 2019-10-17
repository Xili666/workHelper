from logging import Logger

from config.ConfigManager import ConfigManager
from plugin.PluginManager import PluginManager


class AtsPlugin(object):
    def __init__(self, config: ConfigManager, logger: Logger):
        self.config = config
        self.pm = PluginManager.get_plugin_manager()
        self.redis_plugin = self.pm.get_plugin('redis')
        self.zk_plugin = self.pm.get_plugin('zookeeper')
        self.uq_plugin = self.pm.get_plugin('uniqueCode')
        pass

    def start(self, args=None):
        use_docker = self.config.get_config('ats.redis.docker.useDocker')
        if not use_docker:
            self.redis_plugin.rdb('remove')
        self.redis_plugin.start()
        self.zk_plugin.start()
        self.uq_plugin.start()

    def stop(self, args=None):
        self.redis_plugin.stop()
        self.zk_plugin.stop()
        self.uq_plugin.stop()
