import os
from tkinter import Tk
from tkinter.messagebox import showinfo

def fn():
    root=Tk()
    os.system("control mmsys.cpl sounds,1")
    showinfo(
        title='Stereo Mix',
        message="Please enable Stereo Mix Sound Device"
        )
    showinfo(
        title='Close',
        message="Please Reopen the app again!"
    )
    root.destroy()

if __name__=="__main__":
    fn()