from logging import Logger

from config.ConfigManager import ConfigManager


class UcPlugin(object):
    __doc__ = '''
    UC插件:
    config: dbusername=xxx dbpassword=jats002
    '''

    def __init__(self, config: ConfigManager, logger: Logger):
        self.uc_path = config.get_config('ats.uc.path')
        self.logger = logger
        pass

    def config(self, args=None):
        _dir = dict()
        for part in args:
            kv = part.split('=', 1)
            _dir[kv[0]] = kv[1]
        config_lines = list()
        with open('{}/config.properties'.format(self.uc_path), mode='r', encoding='utf-8') as f:
            for line in f:
                config_lines.append(line)
        pass
        for index in range(0, len(config_lines)):
            for k, v in _dir.items():
                if config_lines[index].startswith(k):
                    config_lines[index] = '{}={}\n'.format(k, v)
                    break
        pass
        with open('{}/config.properties'.format(self.uc_path), mode='w', encoding='utf-8') as f:
            for line in config_lines:
                f.write(line)
        pass
