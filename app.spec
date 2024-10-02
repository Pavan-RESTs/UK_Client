# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['run.py'],
             pathex=[],
             binaries=[],
             datas=[('templates', 'templates'), 
                    ('static', 'static'), 
                    ('colors', 'colors'),
                    ('Luxi-Mono', 'Luxi-Mono'),
                    ('Noto_Sans_Tamil', 'Noto_Sans_Tamil'),
                    ('core_file.py', '.'),
                    ('house_with_dot.jpg', '.')],
             hiddenimports=['engineio.async_drivers.threading'],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='YourAppName',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )