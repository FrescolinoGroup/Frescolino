#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 
# Author:  Mario S. Könz <mskoenz@gmx.net>
# Date:    20.09.2016 17:30:42 CEST
# File:    generate_readme.py

import os
import requests

path = os.path.dirname(os.path.abspath(__file__)) 

def check_url(url):
    request = requests.get(url)
    return (request.status_code == 200)

def main():
    
    travis = []
    
    for mod in sorted(os.listdir(path + "/modules")):
        if check_url('https://travis-ci.org/FrescolinoGroup/{}'.format(mod)):
            print(mod, "has travis")
            travis.append(mod)
    
    with open(path+"/README.md", "w") as f:
        f.write("Build Status\n")
        f.write("============\n")
        f.write("\n")
        f.write("| | |\n")
        f.write("|-|-|\n")
        for mod in travis:
            f.write("|__{0}__|[![Build Status](https://travis-ci.org/FrescolinoGroup/{0}.svg?branch=master)](https://travis-ci.org/FrescolinoGroup/{0})|\n".format(mod))
    

if __name__ == "__main__":
    main()
