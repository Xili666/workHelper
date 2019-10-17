from util import WinUtil
import logging

logger = logging.getLogger('DockerUtil')


def docker_run(cmd):
    logger.info('执行docker命令 {}'.format(cmd))
    out, err = WinUtil.exec_cmd(cmd)  # 启动docker-redis
    if len(out) == 65 and not len(err):
        return True, out[:-1]
    else:
        return False, err


def docker_stop(container_name):
    out, err = WinUtil.exec_cmd('docker stop {}'.format(container_name))
    if out.startswith(container_name):
        out, err = WinUtil.exec_cmd('docker rm {}'.format(container_name))
        if out.startswith(container_name):
            return container_name
        else:
            return err
    else:
        return err
