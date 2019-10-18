from config.ConfigManager import ConfigManager
from handler.ProcessHandler import ProcessHandler
from handler.ThreadHandler import ThreadHandler
from plugin.PluginManager import PluginManager
import yaml
import logging
import logging.config


def init_logger(config_path: str):
    with open(config_path, 'r', encoding='utf-8') as cfg:
        cfg_dict = yaml.load(cfg.read(), Loader=yaml.FullLoader)
    logging.config.dictConfig(cfg_dict)
    logging.getLogger("logger").info('加载日志配置完成')


# args 第一个参数作为方法名, 后面的参数作为方法参数
def do_plugin(plugin: object, args: list):
    if len(args) > 0:
        method_name = args[0]
        try:
            method = getattr(plugin, method_name)
            method(args[1:])
        except AttributeError as err:
            logging.getLogger("logger").error(err)
            print('未知的参数: {}'.format(method_name))
        except PermissionError as err:
            logging.getLogger("logger").error(err)
            print('拒绝访问: {}'.format(err.filename))
    else:
        print('缺少必要的参数')
    pass


# 程序退出
def do_exit():
    logging.getLogger('exit').info('正在退出...')
    logging.getLogger("exit").info('程序结束')


def init_handlers():
    ProcessHandler()
    ThreadHandler()


def main(config_path: str, plugins_path: str, logging_path: str):
    init_logger(logging_path)
    init_handlers()
    cm = ConfigManager(config_path)
    pm = PluginManager(plugins_path, cm).get_plugin_manager()
    logging.getLogger("logger").info('插件加载完成')
    while True:
        line = input('WorkHelper >> ')
        words = line.strip('').split(' ')
        cmd = words[0]  # 命令, 同时也是plugin的名字
        if cmd != '':
            if cmd == 'exit':
                do_exit()
                break
            plugin = pm.get_plugin(cmd)
            if plugin is not None:
                do_plugin(plugin, words[1:])
            else:
                print('未知的命令: {}'.format(cmd))
        pass


if __name__ == '__main__':
    main(config_path="application.yaml",
         plugins_path="plugins.properties",
         logging_path="logging.yaml")
