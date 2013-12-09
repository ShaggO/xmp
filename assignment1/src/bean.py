import random
from pycsp.greenlets import *

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

# Pin process
@process
def pin(cin,cout0,cout1, lbin, rbin):
    while True:
        cin()
        if random.uniform(0,1) < 0.5:
            cout0(lbin)
        else:
            cout1(rbin)

# Bin count collector
@process
def binCollector(cin, size, limit = 0):
    total = 0
    data = [0] * size
    try:
        # Collect until limit is reached or retire/poison occurs
        while total < limit or limit == 0:
            binNum = cin()
            data[binNum] += 1
            total += 1
    except ChannelRetireException, ChannelPoisonException:
        # Continue with the above when catching an exception
        pass

    poison(cin)
    print ', '.join(str(x) for x in data)
    print 'Total: %i' % (total)


# Bean Machine initialization function
def beanMachine(levels, nBalls, terminate = 'inject'):
    # Calculate number of pins and channels in the machine
    pins = levels*(levels+1)/2
    nChans = pins+1

    # Set termination variables
    if (terminate == 'inject'):
        nInject = nBalls
        nCount = 0
    elif (terminate == 'count'):
        nInject = 0
        nCount = nBalls

    # Initialize channels
    chans = Channel() * nChans

    # Create arrays of reader and writer endpoints, bin messages to send and
    # initial pin index
    writers = []
    readers = []
    binNumbers = []
    idx = 0

    # Populate arrays initialized above by looping over levels/layers in the
    # bean machine
    for i in range(1,levels+1):
        # Loop over pins in current level/layer
        for j in range(i):
            # Set left and right child index
            lwriter = idx+i
            rwriter = idx+i+1
            if (lwriter > nChans-1):
                lwriter = nChans-1
            if (rwriter > nChans-1):
                rwriter = nChans-1

            # Get children channel writer endpoints
            writers.append(chans[lwriter].writer())
            writers.append(chans[rwriter].writer())

            # Get own channel reader endpoint
            readers.append(chans[idx].reader())

            # Set bin message to send to children
            binNumbers.append(j)
            binNumbers.append(j+1)

            # Increase pin counter
            idx += 1

    # Instantiate bean machine processes in parallel (pins, injector, collector)
    Parallel(
        [pin(readers[i],writers[i*2],writers[i*2+1],binNumbers[i*2],binNumbers[i*2+1]) for i in range(pins)],
        binCollector(chans[nChans-1].reader(), levels+1, nCount),
        ballInject(chans[0].writer(), nInject)
    )

# Problem 1
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

# Problem 2
beanMachine(50, 1000, 'count')
beanMachine(50, 1000, 'inject')

# Problem 3
# Bias oscillator process
#@process
#def biasOscillator()
#    return



shutdown()
