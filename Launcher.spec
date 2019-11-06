# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['Launcher.py'],
             pathex=['E:\\code\\python\\WorkHelper'],
             binaries=[],
             datas=[],
             hiddenimports=[
             'plugin.ats.AtsPlugin',
             'plugin.ats.redis.RedisPlugin',
             'plugin.ats.zookeeper.ZookeeperPlugin',
             'plugin.ats.uniquecode.UniqueCodePlugin',
             'plugin.ats.configcenter.ConfigCenterPlugin',
             'plugin.ats.uc.UcPlugin'
              ],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='WorkHelper',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
