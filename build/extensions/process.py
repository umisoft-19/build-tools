import os
import subprocess
import shutil
import copy 

class BuildExtensions():
    def __init__(self, src_dir, target_dir=None, 
            src_file_paths=[], target_mapping={}):
        
        self.src_dir = src_dir
        self.target_dir = target_dir
        self.src_file_paths = src_file_paths
        self.target_mapping = target_mapping
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(self.base_dir)


    def run(self):
        self.setup_environment()
        self.compile()
        self.rename_extensions()
        self.move_extensions()
        self.cleanup()


    def setup_environment(self):
        self.env = copy.deepcopy(os.environ)
        self.env['build_source_dir'] = self.src_dir
        self.env['build_file_list'] = ";".join(self.src_file_paths)

    def compile(self):
        res = subprocess.run(['python', 'setup.py', 'build_ext'], env=self.env)
        if res.returncode != 0:
            print(res.stdout)
            print(res.stderr)
            raise Exception(' The extensions failed to build correctly')

    def rename_extensions(self):
        self.target_names = []
        ext_path = os.path.join(self.base_dir, 'build', 'lib.win32-3.6')
        for _dir, __, files in os.walk(ext_path):
            for file_name in files:
                new_name = file_name[:file_name.find('.')] + '.pyd'
                self.target_names.append(new_name)
                try:
                    os.rename(os.path.join(ext_path, _dir, file_name), new_name)
                except FileExistsError:
                    os.remove(new_name)
                    os.rename(os.path.join(ext_path, _dir, file_name), new_name)


    def move_extensions(self):
        for fil in self.target_mapping.keys():
            if os.path.exists(os.path.join(self.target_mapping[fil], fil)):
                os.remove(os.path.join(self.target_mapping[fil], fil))
            if not os.path.exists(self.target_mapping[fil]):
                os.makedirs(self.target_mapping[fil])
                
            shutil.move(fil, self.target_mapping[fil])
            #remove the pyc
            suffix = '.pyc' #if fil != 'password_util.pyd' else '.py'
            name = fil.split('.')[0] +  suffix
            try:
                print(os.path.join(self.target_mapping[fil], name))
                os.remove(os.path.join(self.target_mapping[fil], name))
            except:
                pass

    def cleanup(self):
        for f in self.target_names:
            if os.path.exists(f):
                os.remove(f)
        if os.path.exists('build'):
            shutil.rmtree('build')