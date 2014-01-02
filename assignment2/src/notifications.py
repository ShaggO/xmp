from pycsp.greenlets import *
import sys

# Notification receiver
@process
def receiver(cin, output):
    while True:
        # Wait for notification on cin
        msg = cin()
        (action, player) = msg

        # Print if wanted
        if output:
            print('Player %s %s the room' % (player,action))
            sys.stdout.flush()
