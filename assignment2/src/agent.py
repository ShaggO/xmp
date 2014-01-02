from pycsp.greenlets import *
import notifications
import random
import sys
import time

# Agent that moves around and is able to randomly pick up or drop items
@process
def agent(cout, cin, cnote, logName):
    # Possible commands to send
    cmds = ['N','S','E','W']
    items = []

    # Spawn notification receiver
    Spawn(notifications.receiver(cnote,False))
    while True:
        # Walk randomly around and wait 3 seconds in between each command
        cmd = random.choice(cmds)
        cout(cmd)
        ret = cin()
        sleepP(3)

# Allow sleeping for 3 seconds without busy waiting
@io
def sleepP(t):
    time.sleep(t)
