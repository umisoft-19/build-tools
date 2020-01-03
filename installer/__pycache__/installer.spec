# -*- mode: python -*-

block_cipher = None

added_files = [
    ('project/static', 'static'),
    ('project/static', 'project/static'),
    ('project/templates', 'templates'),
    ('project/templates', 'project/templates'),
    ('WebBrowserInterop.x64.dll','.'),
    ('WebBrowserInterop.x86.dll','.'),
]
a = Analysis(['installer.py'],
             pathex=['C:\\Users\\nakamura9a\\Documents\\code\\git\\latrom_build_tools\\build\\installer'],
             binaries=[],
             datas=added_files,
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
          name='installer',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
