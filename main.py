import tkinter
import ui
import threading

root = tkinter.Tk()

game = ui.GameBoard(root)

print('main.py root.mainloop()')
root.mainloop()
print('end main.py')