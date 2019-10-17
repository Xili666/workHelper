import logging

import yaml


class ConfigManager(object):

    def __init__(self, yaml_path):
        self.logger = logging.getLogger('configManager')
        self.logger.info('读取配置文件: {}'.format(yaml_path))
        with open(yaml_path, 'r', encoding='utf-8') as y:
            yaml_text = y.read()
            self.config = yaml.load(yaml_text, Loader=yaml.FullLoader)

    def get_config(self, element):
        config = self.config
        for k in str(element).split('.'):
            config = config.get(k)
        return config
