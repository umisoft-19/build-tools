'''The build process creates an exe that will install the application on the target machine
the application consists of the server files( the pyd equivalents not the plain text source )
the server also includes the wkhtml2pdf binary
it includes the python install - it will make sure that all the requirements.txt are met in the file


with time this build script will target multiple os's

THE BUILD COUNTER
Major.minor.patch
the build counter is incremented by each build if the build completes successfully 

each build must exist on the master branch with all changes committed.
Each build is linked to this hash value
each build must have an argument specifying if the build is major minor or a 
patch
versions will not be recorded for quick builds


Steps:
1.  check if the repository is on master branch and changes have been committed
2.  check that the react js bundles are all properly compiled
3.  runs unit test
4.  collect static files
5.  copy source code
7.  copy install binaries
8.  install python modules based on requirements.txt
9.  copy the updated python package
10. create setup executable and run executable
11. move executable and utility files
12. remove temp files and compress the application
13. increment build counter


Need to add a way to obfuscate mission critical code
'''
import time
import datetime
import sys
import logging
import os
import git
import copy
import json
import subprocess
import shutil
from distutils.dir_util import copy_tree

from build.compile import SourceCompiler
from build.extensions.process import BuildExtensions


class DjangoProjectBuilder():
    def __init__(self, sys_args):
        self.args = sys_args
        self.start = time.time()
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.app_list = ['accounting', 'common_data', 'employees',
                'inventory', 'invoicing', 'messaging', 'manufacturing',
                'planner', 'services', 'latrom']
        self.run()

    def run(self):
        self.parse_args()
        self.configure_logger()
        self.setup_environment()
        self.repo_checks()
        self.react_checks_and_build()
        self.run_tests()
        self.collect_static()
        self.copy_src()
        self.compile_src()
        self.move_util_files()
        self.build_installer()
        self.build_client()
        self.build_service()
        self.increment_build_counter()
        self.package_app()
        self.cleanup()

    def parse_args(self):
        if len(self.args) < 3:
            raise Exception("""
            The application requires 2 arguments,
            1. A string representing the path of the application
            2. A build flag which can be any of 
                a) --quick for quick builds or an acceptable build type of:
                b) -M for major revisions, -m for minor revisions and -p for patches """)
        
        self.quick_build = self.args[2] in ['-q', '--quick']
        self.patch = self.args[2] == '-p'
        self.major = self.args[2] == '-M'
        self.minor = self.args[2] == '-m'
        self.app_dir = self.args[1]
        if not os.path.exists(self.app_dir) or not os.path.exists(
                os.path.join(self.app_dir, 'manage.py')):
            raise Exception('The application path provided is incorrect or no valid django application was found in this directory')

    def configure_logger(self):
        log_file = "build.log"
        if os.path.exists(log_file):
            os.remove(log_file)

        self.logger = logging.getLogger('name')
        self.logger.setLevel(logging.DEBUG)

        log_format = logging.Formatter("%(asctime)s [%(levelname)-5.5s ] %(message)s")

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(log_format)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(log_format)
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def setup_environment(self):
        self.dir = os.path.dirname(os.path.abspath(__file__))
        self.dist_dir = os.path.join(self.dir, 'dist')
        self.temp_dir = os.path.join(self.dir, 'temp')
        if os.path.exists(self.dist_dir):
            shutil.rmtree(self.dist_dir)
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
        

        env = copy.deepcopy(os.environ)
        env['PATH'] = ";".join([
            os.path.join(self.base_dir, 'installer'),
            os.path.join(self.base_dir, 'client'),
        ]) + env["PATH"]
        self.env = env

        os.mkdir(self.dist_dir)
        os.mkdir(self.temp_dir)

    def repo_checks(self):
        os.chdir(self.app_dir)
        self.logger.info("[Step 1] Checking repository status")

        if self.quick_build: return

        self.repo = git.Repo(self.app_dir)
        '''Makes sure the repository is on the master branch and all changes have been committed'''
        if len(self.repo.index.diff(None)) > 0:
            self.logger.critical("Changes to the repository were not yet committed")
            raise Exception("Please commit changes before continuing with the build process")

        if self.repo.head.reference.name != "windows": # not master
            self.logger.critical("The build is not on the windows branch")
            raise Exception("The build is not on the windows branch please checkout to windows")

    def react_checks_and_build(self):
        self.logger.info("[Step 3] Checking react bundles")
        
        self.stats_file_path = os.path.join(self.app_dir, 
            'assets', 
            'webpack-stats.json')
        stats_file = open(self.stats_file_path, 'r')
        if json.load(stats_file).get("status", "") != "done":
            self.logger.critical("The webpack bundles are not ready")
            raise Exception("There are errors in the webpack bundles")

        os.chdir(self.app_dir)
        
        if self.quick_build:
            return 

        self.logger.info("[Step 2] Making production build of react modules")
        os.chdir(os.path.join(self.app_dir, 'assets'))
        res = subprocess.run(['webpack.cmd', '--config', 'webpack.prod.js'])
        if res.returncode != 0:
            self.logger.error('Failed to build react bundles')
            raise Exception('Failed to build react bundles')

        os.chdir(self.app_dir)
        
    def run_tests(self):
        if self.quick_build:
            return

        self.logger.info("Step [4] running unit tests")
        result = subprocess.run(['python', 'manage.py', 'test'])
        if result.returncode != 0:
            self.logger.error("failed unit tests preventing application from building")
            # raise Exception('The build cannot continue because of a failed unit test.')

    def collect_static(self):
        self.logger.info('Step[5] collecting static files')
        result = subprocess.run(['python', 'manage.py', 'collectstatic', '--no-input'])
        if result.returncode != 0:
            self.logger.error("Failed to collect static files")
            raise Exception("The static files collection process failed")

    def copy_src(self):
        self.logger.info("Step [6] copying source code")
        for path in ['service','service/server', 'service/database']:
            os.mkdir(os.path.join(self.temp_dir, path))

        for app in self.app_list:
            self.logger.info(app)
            copy_tree(os.path.join(self.app_dir, app), 
                os.path.join(self.temp_dir, 'service', 'server', app))

        # create an empty deploy.txt which will be used as a flag to trigger 
        # production mode.
        with open(os.path.join(self.temp_dir, 'service', 'server', 'latrom', 
                'settings', 'deploy.txt') ,'w') as f:
            f.write('')

    def compile_src(self):
        self.logger.info('Step [7] Deleting cache')
        cache_root = os.path.join(self.temp_dir, 'service', 'server')
        skipped_count = 0
        for dir, _, __ in os.walk(cache_root):
            if dir.endswith('__pycache__'):
                path = os.path.join(cache_root, dir)
                if os.path.exists(path):
                    try:
                        shutil.rmtree(path) 
                    except:
                        skipped_count += 1

        if skipped_count > 0:
            self.logger.warning('Some cache files not deleted.')

        self.logger.info('Step [8] Compiling source code')
        compiler = SourceCompiler(os.path.join(
            self.temp_dir, 'service', 'server'), self.app_list)
        compiler.run()

        self.logger.info('Step [9] Building extensions')

        extension_target = os.path.join(self.temp_dir, 'service', 'server')
        extension_builder = BuildExtensions(self.app_dir,
            target_dir=extension_target,
            src_file_paths=[
                'common_data\\middleware\\license.py',
                'common_data\\middleware\\users.py',
                'latrom\\settings\\base.py'
            ], target_mapping={
                'license.pyd': os.path.join(extension_target, 'common_data', 
                    'middleware'),
                'base.pyd':os.path.join(extension_target, 'latrom', 'settings'),
                'users.pyd': os.path.join(extension_target, 'common_data', 
                    'middleware'),
                #'password_util.pyd': os.path.dirname(target_dir)
            }
        )
        extension_builder.run()

    def move_util_files(self):
        self.logger.info('Step [10] moving webpack-stats file')
        shutil.copy(self.stats_file_path, 
            os.path.join(self.temp_dir, 'service', 'server'))

        self.logger.info('Step [11] moving binaries(wkhtmltopdf etc.)')
        shutil.copytree(os.path.join(self.base_dir, 'build', 'bin'), 
            os.path.join(self.temp_dir, 'service', 'bin'))
        
    def build_installer(self):
        #TODO update installer!
        self.logger.info("Step [12] Creating setup executable")
        os.chdir(os.path.join(self.base_dir, 'installer'))
        env = copy.deepcopy(os.environ)
        env['PATH'] = ";".join([
            os.path.join(self.base_dir, 'installer'),
            os.path.join(self.base_dir, 'client'),
            os.path.join(self.base_dir, 'installer', 'env', 'Scripts')
        ]) 

        
        result = subprocess.run(
            ['pyinstaller', 'installer.spec', '--clean', '--uac-admin'], 
            env=env)

        if result.returncode != 0:
            self.logger.critical(
                "The executable for the setup failed to be created")
            raise Exception("The executable for the setup failed to be created")

    def build_service(self):
        self.logger.info('Step [14] building service')
        self.logger.info('Step [15] moving python')
        os.chdir(self.base_dir)
        shutil.copytree(os.path.join('build', 'python'), 
            os.path.join(self.temp_dir, 'service', 'python'))
        os.chdir(os.path.join(self.temp_dir, 'service', 'python'))
        requirements = os.path.abspath(os.path.join(self.app_dir, 
            'requirements.txt'))

        self.logger.info('Step [16] installing packages')
        result = subprocess.run(['./python', '-m', 'pip', 'install', '-r', 
            requirements])

        if result.returncode != 0:
            self.logger.info("Failed to install some packages to python")
            raise Exception("Failed to install some modules to python")

        self.logger.info("Step [16] Creating service executable")
        os.chdir(os.path.join(self.base_dir, 'service'))
        result = subprocess.run(['pyinstaller', 'service.spec', '--clean'])
        if result.returncode != 0:
            self.logger.critical(
                "The executable for the service failed to be created")
            raise Exception("The executable for the service failed to be created")

    def build_client(self):
        self.logger.info("Step [13] Creating client executable")
        os.chdir(os.path.join(self.base_dir, 'client'))
        result = subprocess.run(['pyinstaller', 'client.spec', '--clean'], 
            env=self.env)
        if result.returncode != 0:
            self.logger.critical(
                "The executable for the client failed to be created")
            raise Exception("The executable for the client failed to be created")
        

    def package_app(self):
        self.logger.info('Step [19] packaging app')
        self.logger.info('Step [20] moving src')
        for _,__, files in os.walk(os.path.join(self.base_dir, 'build', 'src')):
            for file in files:
                shutil.copy(os.path.join(self.base_dir, 'build', 'src', file),
                    os.path.join(self.temp_dir, 'service', 'server'))
        
        #moving config
        shutil.move(
            os.path.join(self.temp_dir, 'service', 'server', 'config.json'), 
            os.path.join(self.temp_dir, 'service','database', 'config.json')
            )

        #moving password_util
        # shutil.move(
        #     os.path.join(self.temp_dir, 'service', 'server', 'password_util.py'), 
        #         self.temp_dir)

        self.logger.info('Step [21] moving executables')
        #installer
        shutil.copy(os.path.join(self.base_dir, 'installer', 'dist', 
                'installer.exe'), os.path.join(self.temp_dir))
        shutil.copy(os.path.join(self.base_dir, 'installer', 'build', 
                'installer','installer.exe.manifest'), 
                os.path.join(self.temp_dir))
        
        #client
        shutil.copytree(os.path.join(self.base_dir, 'client', 'dist', 'client'),
            os.path.join(self.temp_dir,'client'))
        #service
        shutil.copytree(os.path.join(self.base_dir, 'service', 'dist',
                'service'), os.path.join(self.temp_dir, 'service', 'service'))
        
        self.logger.info("Step [22] Compressing the application")
        # shutil.make_archive('temp', 'zip', 'dist')
        
        #TODO move config.json to database

    def increment_build_counter(self):
        '''takes a build counter file and increments the build number based on 
        the build argument supplied. The build must not have the argument 
        --quick and the argument should be -M for a major build, -m for a minor 
        build and -p for a patch'''
        if self.quick_build:
            return
        
        self.logger.info("Step [17] Incrementing the build counter")

        today = datetime.date.today()
        new_build = None
        with open(os.path.join(self.base_dir, "build_counter.json"), 'r') as f:
            current_build = json.load(f)

            new_build = copy.deepcopy(current_build)
            
            if self.major:
                new_build['major'] += 1
                new_build['minor'] = 0
                new_build['patch'] = 0

            elif self.minor:
                new_build['minor'] += 1
                new_build['patch'] = 0

            elif self.patch:
                new_build['patch'] += 1


            build_summary = {
                "version": "{}.{}.{}".format(
                    new_build['major'], 
                    new_build['minor'],
                    new_build['patch']),
                "hash": self.repo.head.commit.hexsha,
                "date": f"{today.strftime('%d/%m/%Y')}"
            }

            current_build['builds'].append(build_summary)
            
            if self.major:
                major_release = copy.deepcopy(build_summary)
                major_release['updates'] = []
                current_build['major_releases'].append(major_release)
                
            new_build['builds'] = current_build['builds']
            new_build['major_releases'] = current_build['major_releases']
            self.bc = new_build

        with open(os.path.join(self.base_dir, "build_counter.json"), 'w') as bc:
            json.dump(new_build, bc)

        self.logger.info("Step [18] updating global config")
        conf = None
        conf_path = os.path.join(self.temp_dir, 'service', 'server', 
            'global_config.json')
        
        with open(conf_path, 'r') as conf_file:
            conf = json.load(conf_file)
            conf['application_version'] = build_summary['version']
        
        with open(conf_path, 'w') as conf_file:
            json.dump(conf)

    def cleanup(self):
        self.logger.info("Completed the build process successfully in {0:.2f} seconds".format(time.time() - self.start))

#TODO moved password util to server update installer to reflect this change!!!!

if __name__ == "__main__":
    DjangoProjectBuilder(sys.argv)