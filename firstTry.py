from tkinter import *
from tkinter import messagebox
top = Tk()


def helloCallBack():
    messagebox.showinfo("Hello Python", "Hello Runoob")


B = Button(top, text="点我", command=helloCallBack)

B.pack()
top.mainloop()