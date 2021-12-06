# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['mainWin.py'],
             pathex=['D:\\Homework\\AI\\Program\\LearnPyQt'],
             binaries=[],
             datas=[("images","images"),("Lib","Lib"),("UI","UI")],
             hiddenimports=['PyQt5'],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=['runtimehook1.py'],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='Analysis-Tool',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='mainWin')
