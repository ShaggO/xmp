import player, room, agent
from pycsp.greenlets import *


##### Initialize player
pChans = Channel() * 10
wInd = lambda(x): 2*x
rInd = lambda(x): wInd(x)+1
pObjects = []
# Initialize player objects for the world
#pObjects.append({
#    'name':  'Malte',
#    'cin':   pChans[wInd(0)].reader(),
#    'cout':  pChans[rInd(0)].writer(),
#    'items': []})
pObjects.append({
    'name':  'Agent #0',
    'cin':   pChans[wInd(1)].reader(),
    'cout':  pChans[rInd(1)].writer(),
    'items': []})
#pObjects.append({
#    'name':  'Agent # 1',
#    'cin':   pChans[wInd(2)].reader(),
#    'cout':  pChans[rInd(2)].writer(),
#    'items': []})
#pObjects.append({
#    'name':  'Agent #  2',
#    'cin':   pChans[wInd(3)].reader(),
#    'cout':  pChans[rInd(3)].writer(),
#    'items': []})
#pObjects.append({
#    'name':  'Agent #   3',
#    'cin':   pChans[wInd(4)].reader(),
#    'cout':  pChans[rInd(4)].writer(),
#    'items': []})

# Initialize player processes
players = []
#players.append(player.player(pChans[0].writer(),pChans[1].reader()))
players.append(agent.agent(pChans[wInd(1)].writer(),pChans[rInd(1)].reader(),'Agent #0'))
#players.append(agent.agent(pChans[wInd(2)].writer(),pChans[rInd(2)].reader(),'Agent # 1'))
#players.append(agent.agent(pChans[wInd(3)].writer(),pChans[rInd(3)].reader(),'Agent #  2'))
#players.append(agent.agent(pChans[wInd(4)].writer(),pChans[rInd(4)].reader(),'Agent #   3'))


##### Initialize world
rChans = Channel() * 8
# Room layout:
#  0  1
#  3  2

# Room 0
rooms = []
rooms.append(room.room(
    'Room #0',
    rChans[rInd(0)].reader(),
    rChans[wInd(0)].reader(),
    {
        'N': None,
        'S': (rChans[rInd(3)].writer(), rChans[wInd(3)].writer()),
        'E': (rChans[rInd(1)].writer(), rChans[wInd(1)].writer()),
        'W': None
    },
    'Possible to move [S] and [E]',
    ['dog','cat','mouse'],
    pObjects))

# Room 1
rooms.append(room.room(
    'Room #1',
    rChans[rInd(1)].reader(),
    rChans[wInd(1)].reader(),
    {
        'N': None,
        'S': (rChans[rInd(2)].writer(), rChans[wInd(2)].writer()),
        'E': None,
        'W': (rChans[rInd(0)].writer(), rChans[wInd(0)].writer())
    },
    'Possible to move [S] and [W]',
    ['gold','frankincense','myrrh']
    ))

# Room 2
rooms.append(room.room(
    'Room #2',
    rChans[rInd(2)].reader(),
    rChans[wInd(2)].reader(),
    {
        'N': (rChans[rInd(1)].writer(), rChans[wInd(1)].writer()),
        'S': None,
        'E': None,
        'W': (rChans[rInd(3)].writer(), rChans[wInd(3)].writer())
    },
    'Possible to move [N] and [W]'
    ))

# Room 3
rooms.append(room.room(
    'Room #3',
    rChans[rInd(3)].reader(),
    rChans[wInd(3)].reader(),
    {
        'N': (rChans[rInd(0)].writer(), rChans[wInd(0)].writer()),
        'S': None,
        'E': (rChans[rInd(2)].writer(), rChans[wInd(2)].writer()),
        'W': None
    },
    'Possible to move [N] and [E]',
    ['gun','knife','tomato']
    ))


# Run the world


Parallel(
    rooms,
    players
)

shutdown()
