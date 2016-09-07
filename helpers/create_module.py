#!/usr/bin/env python3
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

project_dir = os.path.dirname(os.path.abspath(__file__)) + "/.."

# put the organisation to None if you want to create repos as a user instead
#~ organisation = None
organisation = "frescolinogroup"
team_name = "CoreDev"
server = "https://api.github.com"

# to get the team id, use
# curl -u username https://api.github.com/orgs/frescolinogroup/teams
team_id = "1979134"

def remove_remote_repo(name):
    user = input("State your GitHub username: ")
    cmd1 = "curl -s -u {} {}/repos/{}/{} -X DELETE"
    
    if organisation == None:
        cmd1 = cmd1.format(user, server, user, name)
    else:
        cmd1 = cmd1.format(user, server, organisation, name)
    
    confirm = input("You are about to delete the repo {0}, type '{0}' to confirm: ".format(name))
    
    if confirm == name:
        re1 = subprocess.check_output(cmd1, shell=True).decode("utf-8")
        print("Repo {} was deleted".format(name))
    
def create_remote_repo(name):

    # username needs admin rights in the organisation
    user = input("State your GitHub username: ")
    descr = ""
    
    if organisation == None:
        # create the remote repo (-s turns down the progress bar)
        cmd1 = 'curl -s -u {} {}/user/repos -d \'{{"name":"{}","description":"{}"}}\''.format(user, server, name, descr)
    else:
        cmd1 = 'curl -s -u {} {}/orgs/{}/repos -d \'{{"name":"{}","description":"{}","team_id":{}}}\''.format(user, server, organisation, name, descr, team_id)
        

    print("Creating repository on {}".format(server))
    re1 = subprocess.check_output(cmd1, shell=True).decode("utf-8")
    re1 = json.loads(re1)
    
    if "errors" in re1.keys():
        raise RuntimeError("Error: {}!".format(re1["errors"][0]["message"]))
    
    try:
        origin = re1["ssh_url"]
    except KeyError:
        print("ssh_url not found in response from git-server... This was the response:\n{}".format(re1))
    
    if organisation != None:
        # set the admin rights for the team
        cmd2 = 'curl -s -u {} {}/teams/{}/repos/{}/{} -X PUT -d \'{{"permission":"admin"}}\''.format(user, server, team_id, organisation, name)
        print("Setting admin rights for {} team".format(team_name))
        re2 = subprocess.check_output(cmd2, shell=True)

    return origin

def init_git(path, origin):
    subprocess.check_output("git -C {} init".format(path), shell=True)
    try:
        subprocess.check_output("git -C {} remote add origin {}".format(path, origin), shell=True)
    except subprocess.CalledProcessError:
        subprocess.check_output("git -C {} remote rm origin".format(path), shell=True)
        subprocess.check_output("git -C {} remote add origin {}".format(path, origin), shell=True)
    try:
        # this command will fail if there is no commit
        subprocess.check_output("git -C {} log".format(path), shell=True)
        print("Existing Repo found...")
    except subprocess.CalledProcessError:
        subprocess.check_output("git -C {} add '*'".format(path), shell=True)
        subprocess.check_output("git -C {} commit -m 'First automated commit'".format(path), shell=True)
        print("Automatic first commit...")
    
    subprocess.check_output("git -C {} push -u origin master".format(path), shell=True)

def module_exists(name):
    existing_modules = os.listdir(project_dir + '/modules')
    if name in existing_modules:
        return True
    return False


def create_module(name, namespace, lang):

    mod_dest = project_dir+'/modules/' + name
    name_tpl = '{UNDEFINED}'
    namespace_tpl = '{UNDEFINED}'

    if lang == 'python':
        shutil.copytree(project_dir+'/helpers/python_package_template', mod_dest)
        name_tpl = '{FULL_NAME}'
        namespace_tpl = '{IMPORT_NAME}'
        pkg_dest = os.path.join(mod_dest, 'fsc', namespace)
        # rename pkg_tpl to the actual import name in modules/name/fsc
        shutil.move(
            os.path.join(mod_dest, 'fsc', 'pkg_tpl'),
            pkg_dest
        )
        shutil.copytree('python_doc_template', os.path.join(mod_dest, 'doc')) # ToDo: merge with python_package_template

    if lang == 'cpp':
        shutil.copytree(project_dir+'/helpers/cpp_library_template', mod_dest)
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
    
    if module_exists(args.name) or (args.language == 'python' and module_exists(args.namespace)):
        print('Warning: not creating a module with name {}, as it exists already.'.format(args.name))
    else:
        create_module(args.name, args.namespace, args.language)
        print("Created new {}-module {}".format(args.language, args.name))

    # create repo in module directory (can be empty)
    if args.github:
        if module_exists(args.name):
            # create remote repo on FrescolinoGroup / add CoreDev team with admin rights
            origin = create_remote_repo(args.name)
            init_git(project_dir+'/modules/' + args.name, origin)
            # add submodule
            subprocess.check_output("git -C {0} submodule add {1} ./modules/{2}".format(project_dir, origin, args.name), shell=True)
            print("Added {} as a submodule".format(args.name))
            #~ remove_remote_repo(args.name)
        else:
            print("Module {} does not exist!".format(args.name))
