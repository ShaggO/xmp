from pycsp.greenlets import *
import re
import sys
# Room process
@process
def room(name, cin, neighbours, players = None, desc = '', items = None):
    # Setup default list values if not set
    if players is None:
        players = []
    if items is None:
        items = []

    # Loop until exit command is processed or poison occurs
    try:
        while True:
            # Choice between players cin and room input cin
            chan,message = AltSelect(
                    InputGuard(cin),
                    *[InputGuard(p['cin']) for p in players]
                )
            # Message on room cin
            if chan == cin:
                # Notify existing players of new player
                player = message
                notifyPlayers(
                        [p['cnote'] for p in players],
                        ('enters',player['name'])
                )
                # Move player into this room
                players.append(player)

            else:
                # Player command inputted
                player = next((p for p in players if p['cin'] == chan),None)
                cmd = message
                ret = False

                # Move player to adjacent room if it exists
                # The actual move is performed asynchronously to avoid
                # deadlocking
                if cmd in ['N','S','E','W']:

                    nChan = neighbours[cmd]
                    if nChan is not None:
                        players.remove(player)
                        Spawn(moveAgent(nChan, player))

                        # Notify other players in room
                        notifyPlayers(
                            [p['cnote'] for p in players],
                            ('leaves',player['name'])
                        )
                        ret = True

                elif cmd == 'look':
                    # Return a tuple of information about the room when serving
                    # a "look" command
                    ret = (name, desc, players, items)
                elif cmd == 'exit':
                    # Shutdown the MUD and all processes
                    logPrint(name,'Exiting')
                    shutdownMUD(cin, players, neighbours)
                    for p in players:
                        poison(p['cin'])
                        poison(p['cnote'])
                    for r in neighbours.values():
                        if r is not None: poison(r)
                    ret = True
                elif cmd[:4] == 'take':
                    # Associate an item with a player (let the player take it)
                    item = cmd[5:]
                    if item in items:
                        items.remove(item)
                        player['items'].append(item)
                        ret = True
                elif cmd[:5] == 'leave':
                    # Leave an item in the room
                    item = cmd[6:]
                    if item in player['items']:
                        player['items'].remove(item)
                        items.append(item)
                        ret = True

                # Signal player with return value/return control to player
                # process
                player['cout'](ret)

    except ChannelPoisonException:
        # Shutdown the MUD and all processes on poison
        shutdownMUD(cin, players, neighbours)

# Shutdown function which poisons all needed channels
def shutdownMUD(cin, players, neighbours):
    poison(cin)
    for p in players:
        poison(p['cin'])
        poison(p['cnote'])
    for r in neighbours.values():
        if r is not None: poison(r)

# Process for sending a player to another room through cout
@process
def moveAgent(cout, msg):
    cout(msg)

def notifyPlayers(players, message):
    while len(players) > 0:
        g,msg = AltSelect(
            *[OutputGuard(c,msg=message) for c in players]
        )
        players.remove(g)

def logPrint(name,msg):
    print('[%s]: %s' % (name, msg))
    sys.stdout.flush()
    return
