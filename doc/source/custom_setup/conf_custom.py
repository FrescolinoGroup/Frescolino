#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>
# Date:    27.08.2015 19:52:55 CEST
# File:    conf_custom.py

import os

fsc_folder = '../../fsc/'

class Module(object):
    def __init__(self, name):
        self.name = name
        self.doc_folder = fsc_folder + self.name + '/doc/fsc/'

    def create(self):
        raise NotImplementedError

class DoxygenModule(Module):
    def create(self):
        print('Doxygen')
        print(self.name)

class SphinxModule(Module):
    def create(self):
        print('Sphinx')
        print(self.name)

def create_module_files(show_hidden=False):
    tag_switch = {'doxygen': DoxygenModule, 'sphinx': SphinxModule}
    for name in os.listdir(fsc_folder):
        if name.startswith('_') and not show_hidden:
            continue
        for tag, mod in tag_switch.items():
            if os.path.isfile(fsc_folder + name + '/doc/fsc/' + tag + '.tag'):
                mod(name).create()
    print('*' * 100)

    
#~ def get_modules():
#~ 
#~ module_list = [name for name in os.listdir(fsc_folder) if (os.path.isdir(fsc_folder + name) and not name.startswith('_'))]
#~ def module_folder(name):
    #~ return fsc_folder + name + '/'
#~ 
#~ def doc_folder(name):
    #~ return module_folder(name) + 'doc/'
#~ 
#~ def get_modules(tag_name):
    #~ 
#~ 
#~ def main():
#~ 
    #~ doxy_modules = []
    #~ if os.isfile()
#~ 
    #~ sphinx_modules
#~ for module in module_list:
    #~ if os.isfile()    

#~ def clear_modules():
    #~ modules_build = './modules/'
    #~ try:
        #~ shutil.rmtree(modules_build)
    #~ except OSError:
        #~ pass
    #~ os.mkdir(modules_build)
    #~ for module in module_list:
        #~ os.mkdir(modules_build + module)
#~ 
#~ with open('./index_template.rst', 'r') as f:
    #~ index_template = f.read()
#~ with open('./doc_template.rst', 'r') as f:
    #~ doc_template = f.read()
#~ with open('./main_template.rst', 'r') as f:
    #~ main_template = f.read()
#~ 
#~ # create index
#~ module_string = '\n    '.join(['./modules/{name}/main.rst'.format(name=module) for module in module_list])
#~ with open('./index.rst', 'w') as f:
    #~ f.write(index_template.format(modules=module_string))
#~ 
#~ def replace_recursive(old, new, start_folder, modifier):
    #~ print(start_folder)
    #~ print("sed -i 's/" + old + "/" + new + "/g' *.rst")
    #~ subprocess.call("sed -i 's/" + old + "/" + new + "/g' *.rst", cwd=start_folder, shell=True)
    #~ for name in os.listdir(start_folder):
        #~ new_folder = start_folder + '/' + name
        #~ if os.path.isdir(new_folder):
            #~ replace_recursive(old, modifier + new, new_folder, modifier)
#~ 
#~ # create new modules_build files
#~ for module in module_list:
    #~ module_folder = modules_build + module + '/'
    #~ doc_support_folder = module_folder + 'doc/fsc'
    #~ shutil.copytree(fsc_folder + module + '/doc/fsc', doc_support_folder)
    #~ replace_recursive('{PKG_DIR}', '..\/..\/..\/..\/..\/fsc\/' + module, doc_support_folder, '..\/')
    #~ with open(modules_build + module + '/main.rst', 'w') as f:
        #~ f.write(main_template.format(name=module, title_underline="="*len(module)))
    #~ with open(modules_build + module + '/doc.rst', 'w') as f:
        #~ f.write(doc_template.format(name=module, title_underline="="*len(module)))
#~ 
#~ ## ## END CUSTOM SETUP    
