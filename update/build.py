import os
import shutil
import sys
import time
import datetime
import logging
import git
import json
import re
from compile import SourceCompiler
import subprocess

#updates do not include versions of the software where the requirements.txt changes
class BuildException(Exception): pass


class UpdateBuilder():
    def __init__(self, app_path, counter_path, minor=False):
        #assumes an update is a patch unless otherwise stated
        self.minor = minor
        self.start = time.time()
        self.app_path = app_path
        self.counter_path = counter_path
        self.curr_dir = os.path.dirname(os.path.abspath(__file__))
        self.app_list = ['accounting', 'common_data', 'employees',
                'inventory', 'invoicing', 'messaging', 'manufacturing',
                'planner', 'services', 'latrom']

    def run(self):
        self.setup_logger()
        self.setup_repo()
        self.setup_build_counter()
        self.analyse_changes()
        self.create_files()
        self.compile_update()
        self.update_build_counter()
        self.build_update()


    def setup_logger(self):
        log_file = "update_builder.log"
        if os.path.exists(log_file):
            os.remove(log_file)

        self.logger = logging.getLogger('update_builder')
        self.logger.setLevel(logging.DEBUG)

        log_format = logging.Formatter("%(asctime)s [%(levelname)-5.5s ] %(message)s")

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(log_format)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(log_format)
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
        self.logger.info("Step [1] Set up logger successfully")

    def setup_repo(self):
        try:
            self.repo = git.Repo(self.app_path)
            self.logger.info("Step [2] Accessing repository")

        except:
            self.logger.critical("could not access the project repository")
            raise BuildException()
        if len(self.repo.index.diff(None)) > 0:
            self.logger.critical("Changes to the repository were not yet committed")
            raise BuildException()

        if self.repo.head.reference.name != "master":
            self.logger.critical("The build is not on the master branch")
            raise BuildException()

    def setup_build_counter(self):
        self.logger.info("Step [3] Acessing build counter")

        if not os.path.exists(self.counter_path):
            self.logger.critical('The supplied build_counter does not exist')
            raise BuildException()

        with open(self.counter_path, 'r') as bc:
            self.counter= json.load(bc)

        if len(self.counter['major_releases']) == 0:
            self.logger.critical('A major release does not yet exist')
            raise BuildException('Create a major release first before building an update')

        self.previous_major_build = self.counter['major_releases'][-1]

    def analyse_changes(self):
        self.logger.info("Step [4] Analysing build changes")

        self.diffs = self.repo.commit(self.previous_major_build['hash']).diff(self.repo.head.commit.hexsha)
        
        if len(list(self.diffs)) == 0:
            self.logger.warn('There are no changes between the current and the previous build')
            raise BuildException()

        requirements_changes = self.search_diffs(r'^requirements.txt$')
        if len(requirements_changes) > 0:
            self.logger.critical('Cannot update the application with new dependancies.'
            ' Use a major revision to reflect these changes')
            raise BuildException()

    def create_files(self):
        self.logger.info("Step [5] Creating update files")

        self.update_dir = os.path.join(self.curr_dir, 'update')
        files_dir = os.path.join(self.update_dir, 'files')
        if os.path.exists(files_dir):
            shutil.rmtree(files_dir)

        if not os.path.exists(files_dir):
            os.makedirs(files_dir)
        
        fails = []
        delete_list = open(os.path.join(self.update_dir, 'del_list.txt'), 'w')

        for d in [ i for i in self.diffs if 'build' not in i.b_path]:
            if d.change_type in ["D", "R"]:
                delete_list.write(d.b_path + '\n')
            else:
                pathname = d.b_path.replace("/", "\\")
                dest_dir = os.path.join(files_dir, os.path.dirname(pathname))
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                try:
                    shutil.copy(os.path.join(self.app_path, pathname), dest_dir)
                except Exception as e:
                    fails.append(d.b_path)
                    self.logger.error(f'Copy of {d.b_path} failed because of {e}')
                    self.logger.error(d.change_type)

        delete_list.close()

        if fails.__len__() > 0:
            self.logger.warning("{} files failed to copy".format('\n'.join(fails)))
            raise BuildException()

    def compile_update(self):
        SourceCompiler(os.path.join(self.update_dir, 'files'), self.app_list).run()

    def build_update(self):
        res = subprocess.run(['pyinstaller', 'install.spec', '--clean'])
        if res.returncode != 0:
            self.logger.critical('Failed to build update executable')
            raise Exception('Failed to complete build')


    def update_build_counter(self):
        build = {
            'hash': self.repo.head.commit.hexsha,
            'major':self.counter['major'],
            'minor': self.counter['minor'] + 1 if self.minor \
                else self.counter['minor'],
            'patch': 0 if self.minor else self.counter['patch'] + 1,
            'date': datetime.date.today().strftime("%d/%m/%Y")
        }
        summary = {
            'version': f"{build['major']}.{build['minor']}.{build['patch']}",
            'hash': build['hash'],
            'date': build['date']
        }
        self.counter['builds'].append(summary)
        self.counter['major_releases'][-1].setdefault('updates', []).append(summary)
        
        self.counter['minor'] = build['minor']
        self.counter['patch'] = build['patch']
        
        with open(self.counter_path, 'w') as counter_file:
            json.dump(self.counter, counter_file)

        with open('meta.json', 'w') as meta:
            json.dump(summary, meta)

    def search_diffs(self, pattern):
        matches = []
        for diff in self.diffs:
            if re.search(pattern, diff.b_path):
                matches.append(diff.b_path)
        
        return matches


if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise Exception("Build requires at least 2 arguments,"
            " an application path and a build counter path")
    
    is_minor = '-m' in sys.argv
    UpdateBuilder(sys.argv[1], sys.argv[2], minor=is_minor).run()