import tkinter
import ui
import threading

root = tkinter.Tk()

game = ui.GameBoard(root)
game.add_unit(50,50,'red')

print('main.py root.mainloop()')
root.mainloop()
print('end main.py')