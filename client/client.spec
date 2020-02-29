# -*- mode: python -*-
# -*- coding: utf-8 -*-

"""
This is a PyInstaller spec file.
"""

import os
from PyInstaller.building.api import PYZ, EXE, COLLECT
from PyInstaller.building.build_main import Analysis
from PyInstaller.utils.hooks import is_module_satisfies
from PyInstaller.archive.pyz_crypto import PyiBlockCipher

# Constants
DEBUG = os.environ.get("CEFPYTHON_PYINSTALLER_DEBUG", False)
PYCRYPTO_MIN_VERSION = "2.6.1"

# Set this secret cipher to some secret value. It will be used
# to encrypt archive package containing your app's bytecode
# compiled Python modules, to make it harder to extract these
# files and decompile them. If using secret cipher then you
# must install pycrypto package by typing: "pip install pycrypto".
# Note that this will only encrypt archive package containing
# imported modules, it won't encrypt the main script file
# (wxpython.py). The names of all imported Python modules can be
# still accessed, only their contents are encrypted.
SECRET_CIPHER = None#"This-is-a-secret-phrase"  # Only first 16 chars are used

# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

if SECRET_CIPHER:
    # If using secret cipher then pycrypto package must be installed
    if not is_module_satisfies("pycrypto >= %s" % PYCRYPTO_MIN_VERSION):
        raise SystemExit("Error: pycrypto %s or higher is required. "
                         "To install type: pip install --upgrade pycrypto"
                         % PYCRYPTO_MIN_VERSION)
    cipher_obj = PyiBlockCipher(key=SECRET_CIPHER)
else:
    cipher_obj = None

a = Analysis(
    ["client.py"],
    hookspath=["."],  # To find "hook-cefpython3.py"
    cipher=cipher_obj,
    win_private_assemblies=False,#changed
    win_no_prefer_redirects=False,#changed
)

if not os.environ.get("PYINSTALLER_CEFPYTHON3_HOOK_SUCCEEDED", None):
    raise SystemExit("Error: Pyinstaller hook-cefpython3.py script was "
                     "not executed or it failed")

pyz = PYZ(a.pure,
          a.zipped_data,
          cipher=cipher_obj)

exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name="client",
          debug=True,#changed
          strip=False,
          upx=True,
          console=True,
          icon='logo3.ico'
        )
COLLECT(exe,
        a.binaries,
        a.zipfiles,
        a.datas,
        strip=False,
        upx=True,
        name="client")
