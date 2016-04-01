#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>
# Date:    30.03.2016 00:30:19 CEST
# File:    create_python_module.py

import os
import sys
import shutil
import argparse

import subprocess
import json

def create_remote_repo(full_name):
    # to get the team id, use
    # curl -u username https://api.github.com/orgs/frescolinogroup/teams
    # username needs admin rights in the frescolinogroup
    
    user = input("State your GitHub username: ")
    descr = ""
    team_id = "1979134"
    
    # create the remote repo (-s turns down the progress bar)
    cmd1 = 'curl -s -u '+user+' https://api.github.com/orgs/frescolinogroup/repos -d \'{"name":"'+full_name+'","description":"'+descr+'","team_id":'+team_id+'}\''
    
    # set the admin rights for the team
    cmd2 = 'curl -s -u '+user+' https://api.github.com/teams/'+team_id+'/repos/frescolinogroup/'+full_name+' -X PUT -d \'{"permission":"admin"}\''
    
    print("Creating repository on github")
    re1 = subprocess.check_output(cmd1, shell=True).decode("utf-8")
    re1 = json.loads(re1)
    origin = re1["ssh_url"]
    print("Setting admin rights to CoreDev team")
    re2 = subprocess.check_output(cmd2, shell=True)
    
    return origin


def init_git(path, origin):
    subprocess.check_output("git -C {} init".format(path), shell=True)
    subprocess.check_output("git -C {} remote add origin {}".format(path, origin), shell=True)
    subprocess.check_output("git -C {} add '*'".format(path), shell=True)
    subprocess.check_output("git -C {} commit -m 'First automated commit'".format(path), shell=True)
    subprocess.check_output("git -C {} push -u origin master".format(path), shell=True)

def create_module(full_name, import_name):
    existing_modules = os.listdir('../modules')
    for name in [full_name, import_name]:
        if name in existing_modules:
            raise ValueError('A fsc module with name {} exists already'.format(name))

    mod_dest = '../modules/' + full_name
    shutil.copytree('python_package_template', mod_dest)
    pkg_dest = os.path.join(mod_dest, 'fsc', import_name)
    shutil.move(
        os.path.join(mod_dest, 'fsc', 'pkg_tpl'),
        pkg_dest
    )
    
    shutil.copytree('python_doc_template', os.path.join(mod_dest, 'doc'))

    # Replace IMPORT_NAME and FULL_NAME
    for path, _, filenames in os.walk(mod_dest):
        for filename in filenames:
            abspath = os.path.join(path, filename)
            with open(abspath, 'r') as f:
                text = f.read()
            with open(abspath, 'w') as f:
                f.write(text.replace('{IMPORT_NAME}', import_name).replace('{FULL_NAME}', full_name))

    # creating the symlink to the version
    os.symlink(
        '../../version.txt',
        os.path.join(pkg_dest, 'version.txt')
    )
    
    # create remote repo on FrescolinoGroup / add CoreDev team with admin rights
    origin = create_remote_repo(full_name)
    init_git(mod_dest, origin)
    
    # add submodule
    shutil.rmtree(mod_dest)
    subprocess.check_output("git -C ../ submodule add {} ./modules/{}".format(origin, full_name), shell=True)
    
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(dest='full_name', type=str)
    parser.add_argument(dest='import_name', type=str)
    args = parser.parse_args(sys.argv[1:])

    create_module(args.full_name, args.import_name)
