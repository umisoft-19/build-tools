import os
import shutil
from winreg import *
import subprocess
import logging 
import json 
import sys

def resource_path(rel_path):
    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, rel_path)


class UpdateException(Exception): pass

class UmisoftUpdateApp():
    def __init__(self):
        self.curr_dir = os.path.dirname(os.path.abspath(__file__))

    def run(self):
        self.setup_logger()
        try:
            self.set_up_environment()
            self.update_src()
            self.migrate_db()
            self.restart_service()
        except:
            self.logger.exception("The application failed because of the preceding error.")
            self.logger.info('Please share the contents of the file update.log with your application'
                ' vendor for assitance.')
            input('press any key to exit...')
        else:
            self.logger.info("application updated successfully.")
            input("Application updated successfully. Press any key to exit.")

            
    def compare_versions(self, version, update):
        self.logger.info('Installed application version: ', version['application_version'])
        self.logger.info('Update version: ', update['version'])
        v_major, v_minor, v_patch = version['application_version'].split('.')
        u_major, u_minor, u_patch = update['version'].split('.')
        if u_major != v_major:
            self.logger.warn('The major versions are incompatible and'
                ' therefore cannot be used for updates')
            return False

        if u_minor < v_minor:
            self.logger.warn('The minor version of the update is older than the '
                'currently installed version')
            return False

        if u_patch < v_patch:
            self.logger.warn('The patch number is lower for the update than '
                'the currently installed version')
            return False

        return True

    def setup_logger(self):
        log_file = "update.log"
        if os.path.exists(log_file):
            os.remove(log_file)

        self.logger = logging.getLogger('update')
        self.logger.setLevel(logging.DEBUG)

        log_format = logging.Formatter("%(asctime)s [%(levelname)-5.5s ] %(message)s")

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(log_format)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(log_format)
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
        self.logger.info('Logging set up successfully')

    def set_up_environment(self):
        self.logger.info('Accessing application path')
        try:
            key = OpenKey(HKEY_LOCAL_MACHINE, r"SOFTWARE\\umisoft-19")
            self.service_path, _ = QueryValueEx(key, 'SERVICE_PATH')
        except FileNotFoundError:
            self.logger.critical('The application is not installed in the system. Exiting...')
            raise UpdateException('System path is not configured on the system')
        # os.chdir(self.service_path)
        # res = subprocess.run(['service.exe', 'stop'])
        # os.chdir(self.curr_dir)
        
        # self.logger.info('Stopping service...')
        # if res.returncode != 0:
        #     self.logger.critical('Failed to stop application service. Exiting')
        #     raise UpdateException()

        # self.logger.info("Comparing update with current version")
        # with open(os.path.join(
        #         self.service_path, '..', 'server', 'global_config.json'), 'r') as conf:
        #     config = json.load(conf)
        #     meta = None
        #     with open(resource_path('meta.json'), 'r') as meta_f:
        #         self.meta = json.load(meta_f)

        #     valid = self.compare_versions(config, self.meta)
        #     if not valid:
        #         raise UpdateException('The current update is not suitable for the installed applicaiton')

    def update_src(self):
        self.logger.info('Updating application source files')
        with open(resource_path('del_list.txt'), 'r') as del_f:
            for file in del_f:
                path = os.path.join(self.service_path, 'server', file.rstrip())
                if os.path.exists(path):
                    os.remove(path)

    
        #iterates over changed files and replaces the ones in the application 
        # directory
        base_path = resource_path('files')
        for _dir, subdirs, files in os.walk(base_path):
            for file in files:
                # #first remove the existing file in the target
                rel_path = os.path.relpath(_dir, base_path)
                origin = os.path.join(self.service_path, '..', 'server', rel_path,  file)
                dest = os.path.join(self.service_path, '..','server', rel_path)

                if os.path.exists(origin):
                    os.remove(origin)
                # copy the replacement from the files folder into the place of the old 
                # file
                
                if not os.path.exists(dest):
                    os.makedirs(dest)
                shutil.copy(os.path.join(_dir, file), dest)

        self.logger.info("Source files updated successfully")
    
    def migrate_db(self):
        self.logger.info("Migrating database")
        os.chdir(os.path.join(self.service_path,'..', 'server'))
        results = subprocess.run(['../python/python.exe', 'manage.py', 'migrate'])
        if results.returncode != 0:
            self.logger.critical('Could not migrate database')
            raise UpdateException("Failed to migrate database")


    def restart_service(self):
        self.logger.info('Restarting application server')
        os.chdir(self.service_path)
        res = subprocess.run(['service.exe', 'start'])
        if res.returncode != 0:
            self.logger.warn('Failed to restart service. '
                'Please restart your machine to start the applicaiton')


    def update_application_version(self):
        with open(os.path.join(
                self.service_path, '..', 'server', 'global_config.json'), 'r') as conf:
            config = json.load(conf)
            config['application_version'] = self.meta['version']

if __name__ == '__main__':
    
    print('===============================')
    print('          Bentsch Update       ')
    print('===============================')
    print('Please wait while the installer updates your system.')

    app = UmisoftUpdateApp()
    app.run()
    
        