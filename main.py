import tkinter
import ui
from controllib.interface import EthernetServerInterfaceEx
from controllib import event
from collections import defaultdict
import re

root = tkinter.Tk()
root.title('PyBattle')

game = ui.GameBoard(root)

server = EthernetServerInterfaceEx(3888)


buffers = defaultdict(str)
units = defaultdict(lambda:None) #{str(IPAddress): unit()}
@event(server, ['Connected', 'Disconnected'])
def ServerConnectionEvent(client, state):
    print('ServerConnectionEvent(client={}, state={})'.format(client, state))

    if state == 'Connected':
        # A new client has connected, add a new unit for this client
        position = game.GetRandomPosition()
        newColor = game.GetNewColor()
        if newColor is None:
            client.Send('No more positions available')
            client.Disconnect()
        else:
            if units[client.IPAddress] is None:
                newUnit = game.add_unit(position[0], position[1], newColor)
                units[client.IPAddress] = newUnit

    elif state == 'Disconnected':
        buffers.pop(client, None)


moveRE = re.compile('MOVE (UP|DOWN|LEFT|RIGHT)\r')

@event(server, 'ReceiveData')
def ServerRxDataEvent(client, data):
    print('ServerRxDataEvent(client={}, data={})'.format(client, data))
    buffers[client] += data.decode().upper()
    print('buffers[client]=', buffers[client])
    for match in moveRE.finditer(buffers[client]):
        print('match.group(0)=', match.group(0))
        direction = match.group(1)
        unit = units[client.IPAddress]
        unit.move(direction)

        buffers[client] = buffers[client].replace(match.group(0), '')

    if len(buffers[client]) > 10000:
        buffers[client] = ''

server.StartListen()

print('main.py root.mainloop()')
root.mainloop()
server.StopListen()
for client in server.Clients:
    client.Disconnect()
game.GameOver()
print('end main.py')