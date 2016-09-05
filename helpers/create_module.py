#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  C. Frescolino <frescolino@lists.phys.ethz.ch>
# Date:    26.08.2016 19:13:40 CEST
# File:    create_cpp_library.py

import os
import sys
import shutil
import argparse
import time

import subprocess
import json

def create_remote_repo(name):
    # to get the team id, use
    # curl -u username https://api.github.com/orgs/frescolinogroup/teams
    # username needs admin rights in the frescolinogroup

    user = input("State your GitHub username: ")
    descr = ""
    team_id = "1979134"

    # create the remote repo (-s turns down the progress bar)
    cmd1 = 'curl -s -u '+user+' https://api.github.com/orgs/frescolinogroup/repos -d \'{"name":"'+name+'","description":"'+descr+'","team_id":'+team_id+'}\''

    # set the admin rights for the team
    cmd2 = 'curl -s -u '+user+' https://api.github.com/teams/'+team_id+'/repos/frescolinogroup/'+name+' -X PUT -d \'{"permission":"admin"}\''

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

def module_exists(name):
    existing_modules = os.listdir('../modules')
    if name in existing_modules:
        return True
    return False


def create_module(name, namespace, lang):

    if module_exists(name) or (lang == 'python' and module_exists(namespace)):
        print('Warning: not creating a module with name {}, as it exists already.'.format(name))
        return

    mod_dest = '../modules/' + name
    name_tpl = '{UNDEFINED}'
    namespace_tpl = '{UNDEFINED}'

    if lang == 'python':
        shutil.copytree('python_package_template', mod_dest)
        name_tpl = '{FULL_NAME}'
        namespace_tpl = '{IMPORT_NAME}'
        pkg_dest = os.path.join(mod_dest, 'fsc', namespace)
        # rename pkg_tpl to the actual import name in modules/name/fsc
        shutil.move(
            os.path.join(mod_dest, 'fsc', 'pkg_tpl'),
            pkg_dest
        )

    if lang == 'cpp':
        shutil.copytree('cpp_library_template', mod_dest)
        name_tpl = '{LIBRARY_NAME}'
        namespace_tpl = '{NAMESPACE}'
        pkg_dest = os.path.join(mod_dest, 'src', 'fsc', namespace)
        os.makedirs(pkg_dest)

    # replace name and namespace templates
    for path, _, filenames in os.walk(mod_dest):
        for filename in filenames:
            abspath = os.path.join(path, filename)
            with open(abspath, 'r') as f:
                text = f.read()
            with open(abspath, 'w') as f:
                f.write(text.replace(namespace_tpl, namespace).replace(name_tpl, name).replace('{YEAR}', time.strftime('%Y')))

    if lang == 'python':
        # creating the symlink to the version
        os.symlink(
            '../../version.txt',
            os.path.join(pkg_dest, 'version.txt')
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(dest='name', type=str, help='module name')
    parser.add_argument(dest='namespace', type=str, nargs='?', help='module import name / namespace')
    parser.add_argument('language', choices=['python', 'cpp'], nargs='?', help='language template')
    parser.add_argument('--github', action='store_true', help='create a submodule on github (requires rights)')

    args = parser.parse_args()

    if not args.github and not args.language:
        exit('Without --github, both namespace and the language need to be specified!')

    create_module(args.name, args.namespace, args.language)

    # create repo in module directory (can be empty)
    if args.github and module_exists(args.name):
        # create remote repo on FrescolinoGroup / add CoreDev team with admin rights
        origin = create_remote_repo(args.name)
        init_git('../modules/' + args.name, origin)

        # add submodule
        subprocess.check_output("git -C ../ submodule add {} ./modules/{}".format(origin, name), shell=True)