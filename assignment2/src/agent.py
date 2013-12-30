from pycsp.greenlets import *
import notifications
import random
import sys
import time

# Agent that moves around and is able to randomly pick up or drop items
@process
def agent(cout, cin, cnote, logName):
    cmds = ['N','S','E','W']
    items = []
    Spawn(notifications.receiver(cnote,False))
    while True:
        cmd = random.choice(cmds)
        cout(cmd)
        ret = cin()
        sleepP(3)

@io
def sleepP(t):
    time.sleep(t)

def logPrint(name,msg):
    print('[%s]: %s' % (name, msg))
    sys.stdout.flush()
    return
