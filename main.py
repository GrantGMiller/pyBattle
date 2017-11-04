import tkinter
import ui
from controllib.interface import EthernetServerInterfaceEx
from controllib import event
import random

root = tkinter.Tk()

game = ui.GameBoard(root)

server = EthernetServerInterfaceEx(3888)
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
            game.add_unit(position[0], position[1], newColor)

@event(server, 'ReceiveData')
def ServerRxDataEvent(client, data):
    print('ServerRxDataEvent(client={}, data={})'.format(client, data))

server.StartListen()

print('main.py root.mainloop()')
root.mainloop()
print('end main.py')