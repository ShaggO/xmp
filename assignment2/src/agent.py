from pycsp.greenlets import *
import random
import sys
import time

# Agent that moves around and is able to randomly pick up or drop items
@process
def agent(cout, cin, logName):
    #cmds = ['look','exit','N','S','E','W']
    cmds = ['N','S','E','W']
    items = []
    while True:
        cmd = random.choice(cmds)
        cout(cmd)
        ret = cin()

def logPrint(name,msg):
    print('[%s]: %s' % (name, msg))
    sys.stdout.flush()
    return
