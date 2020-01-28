import threading 
import asyncio
import hmac
import re
import shutil
import time
from distutils.dir_util import copy_tree
import requests
import os
import json
import hashlib
import copy
import urllib
import sys
import copy
import subprocess
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from winreg import * 
from project.app_state import application_state, lock
import time
import logging 

logging.basicConfig(filename='debug.log', level=logging.DEBUG)
def generate_hardware_id():
        logging.debug('hardware id')
        result = subprocess.run('wmic csproduct get uuid'.split(), 
            stdout=subprocess.PIPE, 
            stdin=subprocess.PIPE, 
            stderr=subprocess.PIPE, env=os.environ)
        
        _id = result.stdout.decode('utf-8')
        logging.debug(_id)
        _id = _id[_id.find('\n') + 1:]
        id = _id[:_id.find(' ')]
        logging.debug(id)

        return id

def run_checks():

    def write_message(msg):
        lock.acquire()
        application_state['license_check']['message'].append(msg)
        lock.release()
        logging.debug(msg)

    

    def set_retry_state(state):
        lock.acquire()
        application_state['license_check']['retry_active'] = state
        lock.release()
    
    write_message('Checking for license file')
    if not os.path.exists('license.json'):
        write_message("The license file could not be found in the current directory.")
        if os.path.exists("key.txt"):
            write_message('Please email your vendor the file, "key.txt" located to the current directory in order to receive a valid license and proceed')
        else:
            write_message("Attempting to generate a hardware id for license creation.")

            id = generate_hardware_id()
            with open('key.txt', 'w') as f:
                f.write(id)

            write_message('Hardware id generated. Please email the file "key.txt" located in the current directory to your vendor and they will respond with a license file you can copy to the current directory.')
        
        set_retry_state(True)
    
    else:
    
        license = None
        
        with open('license.json') as license_file:
            license = json.load(license_file)
        
        write_message('verifying license.')
    
        #check to see if license file has not been tampered with
        data_string = generate_hardware_id() + json.dumps(license['license'])
        byte_data = bytes(data_string, 'ascii')
        hash = hashlib.sha3_512(byte_data).hexdigest()
    
    
        if not hmac.compare_digest(hash, license['signature']):
            write_message("The license file  in the current directory is invalid. \n Please contact your vendor for assistance")
            set_retry_state(True)
        else:
            write_message('License validated successfully, Click next to continue')
            lock.acquire()
            application_state['license_check']['license_valid'] = True    
            lock.release()
        
        return
    
    

def choose_dir():
    root = Tk()
    path = filedialog.askdirectory()
    lock.acquire()
    application_state['app_location'] = path
    lock.release()
    root.destroy()

def install():
    SYS_PATH = os.environ['path']
    BASE_DIR = os.getcwd()
    TARGET_DIR = application_state['app_location']
    SERVICE_PATH = os.path.join(TARGET_DIR, 'service', 'service')

    ENVIRONMENT = copy.deepcopy(os.environ)
    ENVIRONMENT['PATH'] = ";".join([
        os.path.join(TARGET_DIR, 'service', 'python'),
        os.path.join(TARGET_DIR, 'service', 'python'),
        SERVICE_PATH,
        os.path.join(TARGET_DIR, 'service','bin','wkhtmltopdf', 'bin')])
    print(ENVIRONMENT)
    
    def write_message(msg):
        application_state['install']['messages'].append(msg)
        logging.debug(msg)

    def set_progress(n, success=None):
        application_state['install']['progress'] = n
        application_state['install']['success'] = success

    write_message("Setting up environment")
    set_progress(10)

    if TARGET_DIR != os.getcwd():
        write_message("Copying application files")
        for dir in ['client', 'service']:
            copy_tree(dir, os.path.join(TARGET_DIR, dir))
            
        shutil.copy('password_util.py', TARGET_DIR)
        os.mkdir(os.path.join(TARGET_DIR, 'service','server', 'media'))
        
    target_license = os.path.join(TARGET_DIR, 'service', 'server', 
        'license.json')
    

    shutil.copy(os.path.join(BASE_DIR, 'license.json'), 
        os.path.dirname(target_license)) 
    
    set_progress(40)
    write_message("Installing Visual C++ binaries")
    
    os.chdir(os.path.join(TARGET_DIR, 'service', 'bin'))
    result = subprocess.run('./vc_redist.x64.exe')
    if result.returncode != 0:
        write_message('some dependencies were not properly installed')
        
    set_progress(50)

    os.chdir(TARGET_DIR)
    write_message("Creating superuser")
    try:
        create_superuser(ENVIRONMENT)
    except:
        set_progress(50, success=False)

    set_progress(60)


    os.chdir(os.path.join(TARGET_DIR,'service', 'server'))
    
    write_message("Creating a new database")
    results = subprocess.run(['../python/python.exe', 'manage.py', 'migrate'], 
        env=ENVIRONMENT)

    if results.returncode != 0:
        write_message("Failed to make migrations")
        set_progress(60, success=False)
        return

    set_progress(80)

    write_message("Installing database fixtures")

    results = subprocess.run(['../python/python.exe', 'manage.py', 'loaddata', 'accounts.json', 'journals.json', 'settings.json', 'common.json', 'employees.json', 'inventory.json', 'invoicing.json', 'planner.json', 'payroll.json'], env=ENVIRONMENT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE )


    if results.returncode != 0:
        write_message("Failed to install database")
        set_progress(80, success=False)
        return 

    set_progress(95)
    
    write_message("setting application environment variables")
    #set up a registry value for the application to access when running the service
    #TODO configure service path
    try:
        key = CreateKey(HKEY_LOCAL_MACHINE, r'SOFTWARE\\umisoft-19')
        SetValueEx(key, "SERVICE_PATH", 0, REG_SZ, SERVICE_PATH)
        CloseKey(key)
    except Exception as e:
        set_progress(80, success=False)
        write_message(e)
        write_message('Failed to access registry')
        return 
    
    #! never change 'SBT_PATH' this variable so not to break future updates 
    result = subprocess.run(['service.exe', '--startup=auto', 'install'], 
            env=ENVIRONMENT, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode != 0:
        write_message(result.stdout)
        write_message(result.stderr)
        write_message("Failed to install service")
        set_progress(95, success=False)
        return 

    res = subprocess.run(['service.exe', 'start'], env=ENVIRONMENT)
    if res.returncode != 0:
        write_message("failed to start service, please restart your machine to finish installation.")

    write_message("Installed Application successfully.")
    set_progress(100, success=True)

def create_superuser(env):
    '''edits a the common fixture to include a default superuser as defined by the prompts in the install process'''
    
    BASE_DIR = os.getcwd()
    os.chdir(application_state['app_location'])

    result = subprocess.run(['service/python/python.exe', 'password_util.py', 
        application_state['superuser']['password']], env=env)
    if result.returncode != 0:
        raise Exception("Failed to create password hash")
    with open('hashed_password.txt', 'r') as f:
        password = f.read()

    os.remove('hashed_password.txt')
    os.remove('password_util.py')

    userdata = {
        "model": 'auth.user',
        'pk': 2,
        'fields': {
            'username': application_state['superuser']['username'],
            'password': password,
            'is_superuser': True,
            'is_staff': True,
            'is_active': True
        }
    }
    fixture_path = os.path.join(application_state['app_location'],'service', 
        'server', 'common_data', 'fixtures', 'common.json')
    common_fixture = json.load(open(fixture_path, 'r'))
    common_fixture.append(userdata)
    os.remove(fixture_path)

    json.dump(common_fixture, open(fixture_path, 'w'))

    os.chdir(BASE_DIR)