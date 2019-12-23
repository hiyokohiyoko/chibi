# GUI を作りたい
import sys
from tkinter import Tk, ttk

root = Tk()
btnframe = ttk.frame(root)
def button1_clicked():
    print("大吉")
    root.quit()

btn = ttk.Button(btnframe, text='占い', command=button1_clicked())

btnframe.grid()
btn.grid()
