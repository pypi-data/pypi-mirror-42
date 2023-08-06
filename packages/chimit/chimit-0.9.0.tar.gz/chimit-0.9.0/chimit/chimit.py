#!/usr/bin/env python
"""
CS 2017.5.24
Wraps an arbitrary command line call in:

    clear; time <command>; chime

Which does the following:

    1. clears the terminal window so the command's output can more easily be seen
    2. times the command
    3. calls a chime to notify the user when the command completes

Install dependencies:

    sudo apt install sox vorbis-tools heroes-sound-effects

"""
from __future__ import print_function
import sys
import os
import time

ERROR_CMD = 'play /usr/share/games/heroes/sfx/stop.wav 2>/dev/null'
SUCCESS_CMD = 'ogg123 /usr/share/sounds/ubuntu/notifications/Mallet.ogg 2>/dev/null'

def main():
    if sys.argv[1:] == '--init':
        os.system('sudo apt install sox vorbis-tools heroes-sound-effects')
    else:
        cmd = ' '.join('"%s"' % part if ' ' in part else part for part in sys.argv[1:])
        os.system('clear')
        t0 = time.time()
        status = int(os.system(cmd))
        td = time.time() - t0
        mins = int(td/60.)
        secs = td % 60
        print('real: %im%ss' % (mins, secs))
        if status:
            os.system(ERROR_CMD)
        else:
            os.system(SUCCESS_CMD)

if __name__ == '__main__':
    main()
