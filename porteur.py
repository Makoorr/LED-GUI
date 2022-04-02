import tkinter as tk
from tkinter import ttk
from tkinter import Tk
from tkinter.messagebox import showinfo
import serial.tools.list_ports

def portinput():
        global inp
        global test
        global port
        global root

        ports_ori=serial.tools.list_ports.comports()
        inp=port.get()

        if (inp!=None):
            for port_i, desc, hwid in sorted(ports_ori):
                txt="{}".format(port_i, desc)
                print("txt: ",txt)
                print("inp: ",inp)
                if(inp==txt):
                    print("JAWEK BEHI IMED EZEZ EZHAHAHAHA")
                    test=True
                    showinfo("Done","Arudino's connected on port "+inp)
                else:
                    showinfo("Error","Arduino's port name not found.")
                if(test==True):
                    root.destroy()
                    print("SIUUU")
                    return(inp)

def fn():
    global inp
    global test
    global port
    global root

    root = Tk()
    root.resizable(False,False)
    root.title('Port Name')
    
    port=tk.StringVar()
    test=False

    frm = ttk.Frame(root, borderwidth=150)
    frm.grid()
    ttk.Label(frm, text="Type the arduino's port name (like :  COM11)").grid(column=0, row=0)
    ttk.Label(frm).grid(column=0,row=1)

    ttk.Entry(frm,textvariable=port).grid(column=0, row=2)

    ttk.Label(frm).grid(column=1, row=3)

    ttk.Button(frm, text="Select",command=portinput).grid(column=0, row=4)
    # ttk.Button(frm, text="Quit", command=root.destroy).grid(column=0, row=4)
    
    root.mainloop()

if __name__=="__main__":
    fn()
    