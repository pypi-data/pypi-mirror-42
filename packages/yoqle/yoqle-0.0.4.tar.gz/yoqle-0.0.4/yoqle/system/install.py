import sys
import system
import os
from termcolor import colored
import system
import json
import subprocess

def install():
    system.info()
    print(colored("\tCreating necessary directories...\n", 'cyan'))
    os.makedirs('./system/yoqle-dir')
    print(colored("\tCreating necessary dictionaries...\n", 'magenta'))
    dictionary = {"scripts": [{"id": "!!!@@@@#####", "script": ""}]}
    dictfile = open("./system/yoqle-dir/dictionary.json","w+")
    json.dump(dictionary, dictfile)
    dictfile.close()

def uninstall():
    print(colored("\tRemoving yoqle files...\n", 'red'))
    cmd = subprocess.Popen(('./scripts/uninstall.sh'), shell = True)
    cmd.wait()
    print(colored("\tPress enter to continue...", 'green'))
