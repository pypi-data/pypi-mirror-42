#!/bin/python

import sys
import os
import json
from json import loads
from pyfiglet import Figlet
import subprocess
from termcolor import colored

sys.path.insert(0, './yoqle/system')

import system
import create
import install

def start():
    running = True
    while(running):
        command = input('\t(yoqle): ')
        type(command)

        if command == '.quit':
            running = False
        if command == '.ls':
            system.ls(True)
        if command == '.uninstall':
            install.uninstall()
            sys.exit(0)
        if command == '.create':
            create.create()
        if command == '.info':
            system.info()
        else:
            with open('system/yoqle-dir/dictionary.json', 'r') as f:
                scripts = loads(f.read())['scripts']
                for script in scripts:
                    if script['id'] == command:
                        # subprocess.call([data["om_points"], ">", diz['d']+"/points.xml"])
                        cmd = subprocess.Popen(('./' + script['script']), shell = True)
                        cmd.wait()
                        #print colored("\tPress enter to continue...", 'green')
                        #print colored("\tPress enter to continue...", 'green')
                        print("\tPress enter to continue...")
                #print colored("\tCould not find command '" + command + "'. Use 'help' or 'info' for more.", 'red')

def main():
    argv = sys.argv
    if len(argv) < 2:
        print('Usage: python yoqle \n' +
        '\t--info | information about yoqle\n' +
        '\t--help | show this list of commands\n' +
        '\t--start | enter a yoqle session\n' +
        '\t--create | create a yoqle script\n' +
        '\t--ls | list the commands currently in this yoqle')
        sys.exit(1)

    if not os.path.exists('./system/yoqle-dir'):
        install.install()

    if argv[1] == '--info':
        system.info()

    if argv[1] == '--create':
        create.create()

    if argv[1] == '--ls':
        system.ls(False)

    if argv[1] == '--start':
        start()

if __name__ == '__main__':
    main(sys.argv)
