import os
import subprocess
import logging
#structure
#install.exe
#server
#   |____manage.py
#python
#   |____python.exe
#bin
#   |____vc_redist.x64.exe

class ServiceException(Exception): pass

try:
    result = subprocess.run('bin/vc_redist.x64.exe')

    os.chdir('server')
    results = subprocess.run(['../python/python.exe', 'manage.py', 'migrate'])
    #install binaries

    if results.returncode != 0:
        print('failed to migrate')

    results = subprocess.run(['../python/python.exe', 'manage.py', 'loaddata', 
        'accounts.json', 'journals.json', 'settings.json', 'common.json', 
        'employees.json', 'inventory.json', 'invoicing.json', 'planner.json', 
        'payroll.json'])

    os.chdir('../service')
    print(os.getcwd())
    

    result = subprocess.run(['service.exe', '--startup=auto', 'install'])

    if result.returncode != 0:
        print('failed to install service')
        raise ServiceException('Failed to install')

    res = subprocess.run(['sc', 'start', 'UmisoftService'])
    if res.returncode != 0:
        print('failed to start service')
        raise ServiceException('Failed to start')

except Exception as e:
    print(e)
    logging.exception('an error occurred')
    input('press any key to exit')