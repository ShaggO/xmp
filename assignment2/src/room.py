from pycsp.greenlets import *
import notifications
import re
import sys
# Room process
@process
def room(name, cin, neighbours, players = None, desc = '', items = None):
    if players is None:
        players = []
    if items is None:
        items = []

    try:
        while True:
            chan,message = AltSelect(
                    InputGuard(cin),
                    *[InputGuard(p['cin']) for p in players]
                )
            if chan == cin:
                player = message
                Spawn(notifications.sender([p['cnote'] for p in
                players],('enters',player['name'])))
                players.append(player)

            else:
                player = next((p for p in players if p['cin'] == chan),None)
                cmd = message
                ret = False
                if player is None:
                    logPrint(name, 'Player not found');
                    break

                if cmd in ['N','S','E','W']:

                    nChan = neighbours[cmd]
                    if nChan is not None:
                        players.remove(player)
                        Spawn(moveAgent(nChan, player))
                        Spawn(notifications.sender([p['cnote'] for p in
                            players],('leaves',player['name'])))

                elif cmd == 'look':
                    ret = (name, desc, players, items)
                elif cmd == 'exit':
                    logPrint(name,'Exiting')
                    poison(cin)
                elif cmd[:4] == 'take':
                    item = cmd[5:]
                    if item in items:
                        items.remove(item)
                        player['items'].append(item)
                elif cmd[:5] == 'leave':
                    item = cmd[6:]
                    logPrint(name,'Leave %s' % item)
                    if item in player['items']:
                        player['items'].remove(item)
                        items.append(item)

                player['cout'](ret)

    except ChannelPoisonException:
        poison(cin)
        for p in players:
            poison(p['cin'])
            poison(p['cnote'])
        for r in neighbours.values():
            if r is not None: poison(r)

@process
def moveAgent(cout, msg):
    cout(msg)

def logPrint(name,msg):
    print('[%s]: %s' % (name, msg))
    sys.stdout.flush()
    return
