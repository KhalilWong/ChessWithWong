# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['ChesswithWong.py', 'ai.py', 'colour.py', 'functions.py', 'piece.py', 'player.py', 'settings.py', 'usercontrol.py'],
             pathex=['C:\\Users\\user\\OneDrive\\Python\\Dyeing'],
             binaries=[],
             datas=[],
             hiddenimports=[],
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
          name='ChesswithWong',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
