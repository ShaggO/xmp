import random
from pycsp.greenlets import *

# Process injecting balls
@process
def ballInject(cout, limit = 0, oCout = None):
    # Inject balls into the system
    if limit != 0:
        # Limited injection
        for i in range(0,limit):
            cout('')
            if oCout is not None:
                oCout('')
    else:
        # Unlimited injection
        while True:
            cout('')
            if oCout is not None:
                oCout('')

    # Retire from first pin
    retire(cout)

# Pin process
@process
def pin(cin,cout0,cout1, lbin, rbin, biasIn = None):
    # Initial bias
    bias = 0.5

    while True:
        # Wait for ball
        cin()

        # Get updated bias if needed
        if biasIn is not None:
            bias = biasIn()

        # Propagate ball according to bias
        if random.uniform(0,1) < bias:
            cout0(lbin)
        else:
            cout1(rbin)

# Bin count collector
@process
def binCollector(cin, size, limit = 0, bCin = None):
    # Initialize internal variables
    total = 0
    data = [0] * size
    try:
        # Collect until limit is reached or retire/poison occurs
        while total < limit or limit == 0:
            binNum = cin()
            data[binNum] += 1
            total += 1
    except ChannelRetireException, ChannelPoisonException:
        pass
    # Poison pins upwards
    poison(cin)

    # Poison the bias if defined
    if bCin is not None:
        poison(bCin)

    # Report histogram/results
    print ', '.join(str(x) for x in data)
    print 'Total: %i' % (total)

# Bias oscillator process
@process
def biasOscillator(cin, cout, bias):
    while True:
        g,msg = FairSelect(
            OutputGuard(cout, msg=bias),
            InputGuard(cin)
        )
        if g == cin:
            if bias <= 0.0:
                operation = lambda x: x+0.01
            elif bias >= 0.5:
                operation = lambda x: x-0.01

            # Perform operation on bias
            bias = operation(bias)

# Bean Machine initialization function
def beanMachine(levels, nBalls, terminate = 'inject', bias = None):
    # Calculate number of pins and channels in the machine
    pins = levels*(levels+1)/2
    nChans = pins+1;

    # Add another channel for the bias
    if bias is not None:
        nChans += 2

    # Set termination variables
    if (terminate == 'inject'):
        nInject = nBalls
        nCount = 0
    elif (terminate == 'count'):
        nInject = 0
        nCount = nBalls

    # Initialize channels
    chans = Channel() * nChans

    # Set bias channel variables (reader for the collector and writer for
    # injector)
    if bias is not None:
        biasInCol = chans[nChans-2].reader()
        biasInInj = chans[nChans-2].writer()
    else:
        biasInCol = None
        biasInInj = None

    #Initialize arrays for the pins
    writers = []
    readers = []
    binNumbers = []
    idx = 0
    biasChan = [None] * pins

    # Populate arrays initialized above by looping over
    # levels/layers in the bean machine
    for i in range(1,levels+1):
        # Loop over pins in current level/layer
        for j in range(i):
            # Set left and right child index
            lwriter = idx+i
            rwriter = idx+i+1
            if (lwriter > pins):
                lwriter = pins
            if (rwriter > pins):
                rwriter = pins

            # Get children channel writer endpoints
            writers.append(chans[lwriter].writer())
            writers.append(chans[rwriter].writer())

            # Get own channel reader endpoint
            readers.append(chans[idx].reader())

            # Set bin message to send to children
            binNumbers.append(j)
            binNumbers.append(j+1)

            # Register bias channel reader if needed
            if bias is not None:
                biasChan[idx] = chans[nChans-1].reader()

            # Increase pin counter
            idx += 1

    others = [binCollector(chans[pins].reader(),
                           levels+1, nCount,biasInCol),
              ballInject(chans[0].writer(), nInject,
                         biasInInj)]

    # Initialize network
    if bias is not None:
        others.append(biasOscillator(chans[nChans-2].reader(),
                                     chans[nChans-1].writer(),
                                     bias))

    Parallel(
        [pin(readers[i],writers[i*2],
             writers[i*2+1],
             binNumbers[i*2],
             binNumbers[i*2+1],
             biasChan[i]) for i in range(pins)],
        others
    )


# Problem 1
layers = 2;
nChans = layers*(layers+1)/2 + 2
chan = Channel() * nChans
others = [binCollector(chan[3].reader(), layers+1,100),
            ballInject(chan[0].writer())]

Parallel(
    pin(chan[0].reader(),chan[1].writer(),chan[2].writer(),0,0),
    pin(chan[1].reader(),chan[3].writer(),chan[3].writer(),0,1),
    pin(chan[2].reader(),chan[3].writer(),chan[3].writer(),1,2),
    others
)

# Problem 2
beanMachine(50, 1000, 'count')
beanMachine(50, 1000, 'inject')

# Problem 3
beanMachine(50, 1000, 'count', 0.5)
beanMachine(50, 1000, 'inject', 0.5)

shutdown()
