import subprocess

p = subprocess.run('docker rm yqats-redis', stdout=subprocess.PIPE, encoding='gbk')
print(p.stdout.startswith('yqats-redis'))
