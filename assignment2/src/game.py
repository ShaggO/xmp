import player, room, agent
from pycsp.greenlets import *


##### Initialize player
pChans = Channel() * 12
pObjects = []
# Initialize player objects to be used internally in the rooms/the world
# 1 client and 3 automatic agents
pObjects.append({
    'name':  'Malte',
    'cin':   pChans[0].reader(),
    'cout':  pChans[1].writer(),
    'cnote': pChans[2].writer(),
    'items': ['gold','frankincense','myrrh']})

pObjects.append({
    'name':  'Agent #0',
    'cin':   pChans[3].reader(),
    'cout':  pChans[4].writer(),
    'cnote': pChans[5].writer(),
    'items': []})

pObjects.append({
    'name':  'Agent #1',
    'cin':   pChans[6].reader(),
    'cout':  pChans[7].writer(),
    'cnote': pChans[8].writer(),
    'items': []})

pObjects.append({
    'name':  'Agent #2',
    'cin':   pChans[9].reader(),
    'cout':  pChans[10].writer(),
    'cnote': pChans[11].writer(),
    'items': []})

# Initialize client/player processes
pAgents = []
pAgents.append(player.player(-pChans[0], +pChans[1], +pChans[2]))
pAgents.append(agent.agent(-pChans[3], +pChans[4], +pChans[5], 'Agent #0'))
pAgents.append(agent.agent(-pChans[6], +pChans[7], +pChans[8], 'Agent #1'))
pAgents.append(agent.agent(-pChans[9], +pChans[10], +pChans[11], 'Agent #2'))


##### Initialize world
# Room channels
rChans = Channel() * 4
# Room layout:
#  0  1
#  3  2

# Room 0
# Add all player objects
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


# Run the world in parallel
Parallel(
    rooms,
    pAgents
)

# Mandatory shutdown of PyCSP
shutdown()
