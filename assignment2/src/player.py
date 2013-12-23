import sys
from pycsp.greenlets import *
import time
# Player process
@process
def player(cout, cin):
    cmd = ''

    while cmd != 'exit':

        # New iteration
        cmd = getCmd()

        cout(cmd)
        ret = cin()
        if cmd == 'look':
            (name, desc, players, items) = ret
            fString  = 'Room name:\t%s' % name
            fString += '\nDescription:\t%s' % desc
            fString += '\nItems:'
            for i in range(len(items)):
                fString += '\n\t[%d]: %s' % (i, items[i])
            fString += '\nPlayers:'
            for p in players:
                print(p['items'])
                fString += '\n\t%s\tholding:\t%s' % (p['name'],', '.join(p['items']))
            print(fString)
            sys.stdout.flush()

@io
def getCmd():
    return raw_input("Command: ")
