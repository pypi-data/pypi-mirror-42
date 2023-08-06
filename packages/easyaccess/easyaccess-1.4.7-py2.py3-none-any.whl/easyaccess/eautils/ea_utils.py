from __future__ import print_function
import argparse
import itertools
import sys
import os
import time
import signal
import stat
import easyaccess.eautils.fileio as eafile
import easyaccess.eautils.dircache as dircache


def without_color(line, color, mode=0):
    return line


try:
    from termcolor import colored as with_color

    def colored(line, color, mode=0):
        if mode == 1:
            return with_color(line, color)
        else:
            return line
except ImportError:
    colored = without_color

desfile = os.getenv("DES_SERVICES")
if not desfile:
    desfile = os.path.join(os.getenv("HOME"), ".desservices.ini")
if os.path.exists(desfile):
    amode = stat.S_IMODE(os.stat(desfile).st_mode)
    if amode != 2 ** 8 + 2 ** 7:
        print('Changing permissions to des_service file to read/write by user')
        os.chmod(desfile, 2 ** 8 + 2 ** 7)  # rw by user owner only


def print_exception(pload=None, mode=1):
    (type, value, traceback) = sys.exc_info()
    if pload and (pload.pid is not None):
        os.kill(pload.pid, signal.SIGKILL)
    print()
    print(colored(type, "red", mode))
    print(colored(value, "red", mode))
    print()


config_file = os.path.join(os.environ["HOME"], ".easyaccess/config.ini")
options_prefetch = ['show', 'set', 'default']
options_add_comment = ['table', 'column']
options_edit = ['show', 'set_editor']
options_out = eafile.FILE_EXTS
options_def = eafile.FILE_DEFS
# ADW: It would be better to grab these from the config object
options_config = ['all', 'database', 'editor', 'prefetch', 'histcache', 'timeout',
                  'outfile_max_mb', 'max_rows', 'max_columns',
                  'width', 'max_colwidth', 'color_terminal', 'loading_bar', 'filepath', 'nullvalue',
                  'autocommit', 'compression', 'trim_whitespace', 'desdm_coldefs']
options_config2 = ['show', 'set']
options_app = ['check', 'submit', 'explain']


def read_buf(fbuf):
    """
    Read SQL files, sql statement should end with ';' if parsing to a file to write.
    """
    try:
        with open(fbuf) as f:
            content = f.read()
    except:
        print('\n' + 'Fail to load the file "{:}"'.format(fbuf))
        return ""
    list = [item for item in content.split('\n')]
    newquery = ''
    for line in list:
        if line[0:2] == '--':
            continue
        newquery += ' ' + line.split('--')[0]
    # newquery = newquery.split(';')[0]
    return newquery


class KeyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.exit(2)


def loading():
    char_s = u"\u2606"
    if sys.stdout.encoding != 'UTF-8':
        char_s = "o"
    print()
    spinner = itertools.cycle(list(range(13)) + list(range(1, 14, 1))[::-1])
    line2 = "  Ctrl-C to abort; "
    try:
        while True:
            line = list('    |              |')
            time.sleep(0.1)
            idx = int(next(spinner))
            line[5 + idx] = char_s
            sys.stdout.write("".join(line))
            sys.stdout.write(line2)
            sys.stdout.flush()
            sys.stdout.write('\b' * len(line) + '\b' * len(line2))
    except:
        pass


def complete_path(line):
    line = line.split()
    if len(line) < 2:
        filename = ''
        path = './'
    else:
        path = line[1]
        if '/' in path:
            i = path.rfind('/')
            filename = path[i + 1:]
            path = path[:i]
        else:
            filename = path
            path = './'
    ls = dircache.listdir(path)
    ls = ls[:]
    dircache.annotate(path, ls)
    if filename == '':
        return ls
    else:
        return [f for f in ls if f.startswith(filename)]
