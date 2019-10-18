import os
import subprocess
import time

from util import WinUtil

tomcat_path = 'D:/devTool/apache-tomcat-7.0.85-config-center'
cmd = '{}: & cd {}/bin & {}/bin/startup.bat'.format(tomcat_path.split(':')[0], tomcat_path, tomcat_path)
print(cmd)
os.system(cmd)
time.sleep(20)
pid = WinUtil.get_commandline_pid(tomcat_path)
print(pid)

for p in pid:
    print('taskkill /f /pid {}'.format(p))
    p = subprocess.run('taskkill /f /pid {}'.format(p), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              shell=True, encoding='gbk')
    print(p.stdout, p.stderr)
