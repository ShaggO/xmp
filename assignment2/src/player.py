import sys
from pycsp.greenlets import *
import notifications
import time

# Player process
@process
def player(cout, cin, cnote):
    cmd = ''
    # Spawn asynchronous notification reciver process
    Spawn(notifications.receiver(cnote,True))

    # Perform command until exit cmd wanted (or poison)
    while cmd != 'exit':

        # New iteration
        # Get input from std.in, send it through cout and wait for return value
        # on cin
        cmd = getCmd()
        cout(cmd)
        ret = cin()

        # Format return value if a look is issued
        if cmd == 'look':
            # Format and print return values from look command
            (name, desc, players, items) = ret
            fString  = 'Room name:\t%s' % name
            fString += '\nDescription:\t%s' % desc
            fString += '\nItems:'
            for i in range(len(items)):
                fString += '\n\t[%d]: %s' % (i, items[i])
            fString += '\nPlayers:'
            for p in players:
                fString += '\n\t%s\tholding:\t%s' % (p['name'],', '.join(p['items']))
            print(fString)
            sys.stdout.flush()

# Allow other processes to run while waiting for IO
@io
def getCmd():
    return raw_input("Command: ")
