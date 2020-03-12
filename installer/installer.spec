# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

appdata = [
    ('project/templates', 'templates'),
    ('project/static', 'static'),
    ('project/templates', 'project/templates'),
    ('project/static', 'project/static'),
    ('WebBrowserInterop.x64.dll','.'),
    ('WebBrowserInterop.x86.dll','.'),
]

a = Analysis(['installer.py'],
             pathex=['C:\\Users\\nakamura9a\\Documents\\code\\git\\umisoft\\build-tools\\installer'],
             binaries=[

             ],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=True)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='installer',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , icon='../client/logo3.ico')
