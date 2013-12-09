import random
from pycsp.greenlets import *

# Problem 1 - basic structure
# Process injecting balls
@process
def ballInject(cout, limit = 0):
    # Inject balls into the system
    if limit != 0:
        for i in range(0,limit):
            cout('')
    else:
        while True:
            cout('')
    retire(cout)

# Basic pin process
@process
def pin(cin,cout0,cout1, lbin, rbin):
    while True:
        cin()
        if random.uniform(0,1) < 0.5:
            cout0(lbin)
        else:
            cout1(rbin)

# Process for bin counting
@process
def binCollector(cin, size, limit = 0):
    total = 0
    data = [0] * size
    try:
        while total < limit or limit == 0:
            binNum = cin()
            data[binNum] += 1
            total += 1
    except ChannelRetireException, ChannelPoisonException:
        pass

    poison(cin)
    print ', '.join(str(x) for x in data)
    print 'Total: %i' % (total)


def beanMachine(levels, nBalls, terminate = 'inject'):
    pins = levels*(levels+1)/2
    nChans = pins+1
    if (terminate == 'inject'):
        nInject = nBalls
        nCount = 0
    elif (terminate == 'count'):
        nInject = 0
        nCount = nBalls

    chans = Channel() * nChans
    writers = []
    readers = []
    binNumbers = []
    idx = 0
    for i in range(1,levels+1):
        for j in range(i):
            lwriter = idx+i
            rwriter = idx+i+1
            if (lwriter > nChans-1):
                lwriter = nChans-1
            if (rwriter > nChans-1):
                rwriter = nChans-1

            writers.append(chans[lwriter].writer())
            writers.append(chans[rwriter].writer())
            readers.append(chans[idx].reader())
            binNumbers.append(j)
            binNumbers.append(j+1)
            idx += 1

    Parallel(
        [pin(readers[i],writers[i*2],writers[i*2+1],binNumbers[i*2],binNumbers[i*2+1]) for i in range(pins)],
        binCollector(chans[nChans-1].reader(), levels+1, nCount),
        ballInject(chans[0].writer(), nInject)
    )


# Problem 3
# Bias oscillator process
#@process
#def biasOscillator()
#    return

layers = 2;

nChans = layers*(layers+1)/2 + 1

chan = Channel() * nChans

Parallel(
    pin(chan[0].reader(),chan[1].writer(),chan[2].writer(),0,0),
    pin(chan[1].reader(),chan[3].writer(),chan[3].writer(),0,1),
    pin(chan[2].reader(),chan[3].writer(),chan[3].writer(),1,2),
    binCollector(chan[3].reader(), layers+1),
    ballInject(chan[0].writer(),100)
)

beanMachine(2, 100, 'count')

shutdown()
