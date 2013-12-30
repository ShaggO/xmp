from pycsp.greenlets import *
import sys

@process
def receiver(cin, output):
    while True:
        msg = cin()
        (action, player) = msg
        if output:
            print('Player %s %s the room' % (player,action))
            sys.stdout.flush()
