from winreg import *
import shutil
import os
import time
from tkinter import filedialog
from tkinter import Tk
import json 
import subprocess

#identify the application directory in the registry
#set a prompt to select the database file
#extract the file
#update database config
#install a new database
#clean up

class DBToolException(BaseException):
    pass

class DBTool():
    def __init__(self):
        pass

    def run(self):
        self.setup_environment()
        self.render()
        self.validate_selection()
        self.install_db()
        self.cleanup()

    def setup_environment(self):
        try:
            key = OpenKey(HKEY_LOCAL_MACHINE, r"SOFTWARE\\umisoft-19")
            self.service_path, _ = QueryValueEx(key, 'SERVICE_PATH')
        except FileNotFoundError:
            raise DBToolException('System path is not configured on the system')
        
        self.app_path = os.path.dirname(self.service_path)

        
    def render(self):
        print('Bentsch Business Tools.')
        print('-----------------------')
        print('This tool will restore a backup of your choice to your application located at: ')
        print(self.app_path)
        input('Press any key to continue: ')
        root = Tk()
        self.backup = filedialog.askopenfilename()
        root.destroy()



    def validate_selection(self):
        filename = os.path.basename(self.backup)
        if not filename.startswith('bkup') or \
                not filename.endswith('.zip'):
            raise DBToolException('The selected file is invalid. It should take the form of '
                'bkup....zip')



    def install_db(self):
        #change config.json in database dir
        os.chdir(os.path.join(self.app_path, 'database'))
        filename_root = os.path.basename(self.backup).strip('.zip')
        timestamp = filename_root.strip('bkup_')
        conf = None
        with open('config.json', 'r') as fr:
            conf = json.load(fr)

        # self.current = conf['current']
        # print('backup current db')
        # ret = subprocess.run('python manage.py dumpdata -o ' + 'temp_backup.json')
        # if ret.returncode == 0:
        #     print('created temp backup')

        conf['current'] = 'db_' + timestamp

        with open('config.json', 'w') as fw:
            json.dump(conf, fw)

        
        #migrate new database
        os.chdir(os.path.join(self.app_path, 'server'))
        ret = subprocess.run('python manage.py migrate')
        if ret.returncode != 0:
            raise DBToolException('Failed to migrate new database')

        #load fixture
        shutil.unpack_archive(self.backup, '.')
        ret = subprocess.run('python manage.py loaddata data.json')
        if ret.return_code != 0:
            # print('restoring temp backup')
            raise DBToolException('Failed to install fixture')



    def cleanup(self):
        os.remove('data.json')
        print('restored backup sucessfully.')
        input('Press any key to exit.')



try:
    DBTool().run()
except DBToolException as e:
    print('The application failed to restore the database for the following reason:')
    print(e)
    input('Press any key to exit.')