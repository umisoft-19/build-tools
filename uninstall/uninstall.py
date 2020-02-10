import os
import shutil
from winreg import *
import subprocess
import sys

print('Uninstalling Bentsch')

answer = ""

while answer.lower() not in ['yes', 'no']:
    answer = input("Are you sure you want to remove the program from your system? yes|no: ")


if answer == "no":
    input('Operation cancelled. Exiting. Press any key to continue.')
    sys.exit()


key = OpenKey(HKEY_LOCAL_MACHINE, r"SOFTWARE\\umisoft-19")
val, reg_type = QueryValueEx(key, 'SERVICE_PATH')
WORKING_DIR = os.path.abspath(os.path.dirname(val)) 

os.chdir(WORKING_DIR)
res = subprocess.run(['sc', 'stop', 'UmisoftService'])
# if res.returncode !=0:
#     input('error stopping service. Exiting press any key to continue')
#     sys.exit()


res = subprocess.run(['sc', 'delete', 'UmisoftService'])
if res.returncode !=0:
    input('error removing service. Exiting press any key to continue')
    sys.exit()


os.chdir('..')
path = os.getcwd()
print(path)
os.chdir('..')
shutil.rmtree(path)

input('sucessfully removed bentsch. Press any key to exit.')