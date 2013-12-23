from pycsp.greenlets import *
import sys

@process
def sender(couts,message):
    while len(couts) > 0:
        g,msg = AltSelect(
            *[OutputGuard(c,msg=message) for c in couts]
        )
        couts.remove(g)

@process
def receiver(cin, output):
    while True:
        msg = cin()
        (action, player) = msg
        if output:
            print('Player %s %s the room' % (player,action))
            sys.stdout.flush()
