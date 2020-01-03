import setuptools
from distutils.core import setup
from Cython.Build import cythonize
import sys 
import os


BASE_DIR = os.environ['build_source_dir']

HARD_COMPILE_FILES = os.environ['build_file_list'].split(';')
HARD_COMPILE_FILES = [os.path.join(BASE_DIR, i) for i in HARD_COMPILE_FILES]
#HARD_COMPILE_FILES.append('password_util.py')

HARD_COMPILE_FILES = [i for i in HARD_COMPILE_FILES if os.path.exists(i)]

setup(
    ext_modules=cythonize(HARD_COMPILE_FILES)
)