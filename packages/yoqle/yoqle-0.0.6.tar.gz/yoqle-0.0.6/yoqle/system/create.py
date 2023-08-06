import sys
import os
import json
from json import loads
from pyfiglet import Figlet
import subprocess
from termcolor import colored
import system

#sys.path.insert(0, './yoqle-dir')

def create():
    #{"scripts": [{"id": "!!!@@@@#####", "script": ""}]}
    name = input('Name of Shortcut: ')
    type(name)
    scriptLoc = input('Location of Script: ')
    type(scriptLoc)

    dictionary = {}

    with open('./yoqle/system/yoqle-dir/dictionary.json', 'r') as f:
        create = 1

        dictionary = loads(f.read())
        scripts = dictionary['scripts']

        for script in scripts:
            if script['id'] == name:
                create = 0

        if create == 1:
            (scripts).append({
                'id': name,
                'script': scriptLoc
            })

        f.close()

    with open('./system/yoqle-dir/dictionary.json', 'w') as outfile:
        json.dump(dictionary, outfile)
