import tkinter
import ui
from controllib.interface import EthernetServerInterfaceEx
from controllib import event
from collections import defaultdict
import re
import hashlib

WELCOME_MESSAGE = '''\
Welcome to PyBattle.

You can move your unit with one of the following commands:
MOVE UP\\r
MOVE DOWN\\r
MOVE LEFT\\r
MOVE RIGHT\\r

You can shoot at other units with the following command:
SHOOT [direction]\\r
    where direction is the angle in degrees.
Examples:
SHOOT 0\\r #Shoots Right
SHOOT 90\\r #Shoots Up
SHOOT 180\\r #Shoot Left
SHOT 270\\r #Shoot Down

You can request a snapshot of the game with this command:
SNAPSHOT\\r
\r\n\r\n
'''

root = tkinter.Tk()
root.title('PyBattle')

game = ui.GameBoard(root)

server = EthernetServerInterfaceEx(3888)

buffers = defaultdict(str)
username = defaultdict(str)
password = defaultdict(str)

units = defaultdict(lambda: None)  # {str(IPAddress): unit()}


@event(server, ['Connected', 'Disconnected'])
def ServerConnectionEvent(client, state):
    print('ServerConnectionEvent(client={}, state={})'.format(client, state))

    if state == 'Connected':
        # A new client has connected, add a new unit for this client
        client.Send(WELCOME_MESSAGE)

        position = game.GetRandomPosition()
        newColor = game.GetNewColor()
        if newColor is None:
            client.Send('No more positions available')
            client.Disconnect()
        else:
            client.Send('You are the {} unit.\r\n'.format(newColor))
            if units[client.IPAddress] is None:
                newUnit = game.add_unit(position[0], position[1], newColor)
                units[client.IPAddress] = newUnit

    elif state == 'Disconnected':
        buffers.pop(client, None)


moveRE = re.compile('MOVE (UP|DOWN|LEFT|RIGHT)\r')
shootRE = re.compile('SHOOT (\d{1,})\r')
snapshotRE = re.compile('SNAPSHOT\r')
userRE = re.compile('USER:(.+?)\r')
passRE = re.compile('PASS:(.+?)\r')


@event(server, 'ReceiveData')
def ServerRxDataEvent(client, data):
    print('ServerRxDataEvent(client={}, data={})'.format(client, data))
    buffers[client] += data.decode().upper()
    print('buffers[client]=', buffers[client])
    for regex in [moveRE, shootRE, snapshotRE, userRE, passRE]:
        for match in regex.finditer(buffers[client]):
            print('match.group(0)=', match.group(0))
            if regex is moveRE:
                direction = match.group(1)
                unit = units[client.IPAddress]
                unit.move(direction)
            elif regex is shootRE:
                direction = match.group(1)
                unit = units[client.IPAddress]
                unit.Shoot(direction)

            elif regex is snapshotRE:
                allUnits = game.GetAllUnits()
                for unit in allUnits:
                    msg = 'Type: {}, UnitID: {}, Color: {}, xPosition: {}, yPosition: {}\r\n'.format(
                        unit.Type,
                        unit._item_number,
                        unit.color,
                        round(unit.x, 2),
                        round(unit.y, 2),
                    )
                    client.Send(msg)

            elif regex is userRE:
                username[client] = match.group(1)
                VerifyUser(client)

            elif regex is passRE:
                password[client] = match.group(1)
                VerifyUser(client)

            buffers[client] = buffers[client].replace(match.group(0), '')

    if len(buffers[client]) > 10000:
        buffers[client] = ''

def VerifyUser(client):
    pw = password[client]
    if pw is not '':
        print('pw=', pw)
        hashed = HashIt(pw)
        print('hash=', hashed)

def HashIt(s):
    print('HashIt(s={})'.format(s))
    return hashlib.sha512(s.encode()).hexdigest()

@event(game, 'UnitDied')
def UnitDiedEvent(deadUnit, killedByUnit):
    print('UnitDiedEvent(deadUnit={}, killedByUnit={})'.format(deadUnit.color, killedByUnit.color))
    if deadUnit in units.values():
        # Notify the user that they have died.
        diedIP = None
        killedByIP = None
        for ip, u in units.items():
            if u == deadUnit:
                diedIP = ip
            elif u == killedByUnit:
                killedByIP = ip

        print('diedIP=', diedIP)
        print('killedByIP=', killedByIP)

        for client in server.Clients:
            if client.IPAddress == diedIP:
                client.Send('You were killed by the {} unit.\r\n:-(\r\n'.format(killedByUnit.color))
                units.pop(client.IPAddress, None)
                # client.Disconnect()

            elif client.IPAddress == killedByIP:
                client.Send('You killed the {} unit.\r\n'.format(deadUnit.color))

            else:
                client.Send('The {} unit killed the {} unit.\r\n'.format(killedByUnit.color, deadUnit.color))



server.StartListen()

print('main.py root.mainloop()')
root.mainloop()
server.StopListen()
for client in server.Clients:
    client.Disconnect()
game.GameOver()
print('end main.py')
