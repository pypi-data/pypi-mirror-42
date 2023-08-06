import sys
import json
from json import loads
from pyfiglet import Figlet
from termcolor import colored

f = Figlet(font='bulbhead')

def info():
    print(f.renderText('yoqle'))
    with open('README.MD', 'r') as fin:
        print(fin.read())

def help():
    with open('help.txt', 'r') as fin:
        print(fin.read())

def ls(fromSession):
    with open('./yoqle/system/yoqle-dir/dictionary.json', 'r') as f:
        scripts = loads(f.read())['scripts']
        for script in scripts:
            if script['id'] != "!!!@@@@#####":
                if fromSession == True:
                    print('\t\t' + script['id'] + ' | ' + script['script'])
                else:
                    print('\t' + script['id'] + ' | ' + script['script'])
        f.close()
