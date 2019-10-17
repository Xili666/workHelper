import importlib
import logging

from config.ConfigManager import ConfigManager


class PluginManager(object):
    __singleton = None

    def __new__(cls, *args, **kwargs):
        if not cls.__singleton:
            cls.__singleton = object.__new__(cls)
        return cls.__singleton

    def __init__(self, prop_path: str, config_manager: ConfigManager):
        self.logger = logging.getLogger('pluginManager')
        self.logger.info('加载配置文件: {}'.format(prop_path))
        self.plugins = dict()
        with open(prop_path, 'r', encoding='utf-8') as p:
            for line in p:
                kv = line.rstrip('\n').split(sep='=', maxsplit=1)
                if len(kv) == 2:
                    module = importlib.import_module('plugin.' + kv[1])
                    ps = kv[1].rsplit('.', 1)
                    if len(ps) == 1:
                        plugin_name = ps[0]
                    else:
                        plugin_name = ps[1]
                    plugin = getattr(module, plugin_name)
                    self.plugins[kv[0]] = plugin(config_manager, logging.getLogger(kv[0]))
                    self.logger.info('插件加载成功: {} \t {}'.format(kv[0], self.plugins[kv[0]]))
                else:
                    self.logger.warning('无效的配置: {}'.format(line))

    @staticmethod
    def get_plugin_manager():
        return PluginManager.__singleton

    def get_plugin(self, name):
        return self.plugins.get(name, None)
