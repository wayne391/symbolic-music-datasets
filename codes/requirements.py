import pip
import importlib

def check_requirements(modules):
    for package in modules:
        pip.main(['install', package])

if __name__ == '__main__':
    modules = ['pafy', 'ffmpy', 'youtube-dl', 'lxml']
    check_requirements(modules)
    print('\n\nDone!!')