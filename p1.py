from tkinter import *
import another

root = Tk()

button1 = Button(root, text = "Call" , command = another.abc)
button1.pack()

root.mainloop()