import player, room, agent
from pycsp.greenlets import *


##### Initialize player
pChans = Channel() * 8
pObjects = []
# Initialize player objects for the world
pObjects.append({
    'name':  'Malte',
    'cin':   pChans[0].reader(),
    'cout':  pChans[1].writer(),
    'items': ['gold','frankincense','myrrh']})

pObjects.append({
    'name':  'Agent #0',
    'cin':   pChans[2].reader(),
    'cout':  pChans[3].writer(),
    'items': []})

pObjects.append({
    'name':  'Agent #1',
    'cin':   pChans[4].reader(),
    'cout':  pChans[5].writer(),
    'items': []})

pObjects.append({
    'name':  'Agent #2',
    'cin':   pChans[6].reader(),
    'cout':  pChans[7].writer(),
    'items': []})

# Initialize player processes
pAgents = []
pAgents.append(player.player(pChans[0].writer(), pChans[1].reader()))
pAgents.append(agent.agent(pChans[2].writer(), pChans[3].reader(), 'Agent #0'))
pAgents.append(agent.agent(pChans[4].writer(), pChans[5].reader(), 'Agent #1'))
pAgents.append(agent.agent(pChans[6].writer(), pChans[7].reader(), 'Agent #2'))


##### Initialize world
# Room channels
rChans = Channel() * 4
# Room layout:
#  0  1
#  3  2

# Room 0
rooms = []
rooms.append(room.room(
    'Room #0',
    rChans[0].reader(),
    {
        'N': None,
        'S': rChans[3].writer(),
        'E': rChans[1].writer(),
        'W': None
    },
    pObjects,
    'Entrance'
    ))

# Room 1
rooms.append(room.room(
    'Room #1',
    rChans[1].reader(),
    {
        'N': None,
        'S': rChans[2].writer(),
        'E': None,
        'W': rChans[0].writer()
    },[],
    'Just another ordinary room'
    ))

rooms.append(room.room(
    'Room #2',
    rChans[2].reader(),
    {
        'N': rChans[1].writer(),
        'S': None,
        'E': None,
        'W': rChans[3].writer()
    },[],
    'Great room'
    ))

# Room 3
rooms.append(room.room(
    'Room #3',
    rChans[3].reader(),
    {
        'N': rChans[0].writer(),
        'S': None,
        'E': rChans[2].writer(),
        'W': None
    },[],
    'A wonderful room'
    ))


# Run the world


Parallel(
    rooms,
    pAgents
)

shutdown()
