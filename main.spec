# -*- mode: python ; coding: utf-8 -*-

from kivy_deps import (sdl2, glew)
from kivymd import hooks_path as kivymd_hooks_path
block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\Users\\DarkLab\\OneDrive\\Projects\\GIE\\GIE_11_03_2021'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[kivymd_hooks_path],
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
          [],
          exclude_binaries=True,
          name='GIE Djiguiya',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe, Tree('C:\\Users\\DarkLab\\OneDrive\\Projects\\GIE\\GIE_11_03_2021'),
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               upx_exclude=[],
               name='GIE Djiguiya')
