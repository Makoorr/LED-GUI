import tkinter as tk
from tkinter import Tk, ttk
from tkinter.messagebox import showinfo

import serial.tools.list_ports

def ports():
    L=[]

    ports_ori=serial.tools.list_ports.comports()
    # for testing:
    # ports_ori=[["COM1","Arduino Port (COM1)","[ACPI\PNP0501\1]"],["COM7", "MediaTek USB Port (COM7)", "[USB VID:PID=0E8D:0003 SER=6 LOCATION=1-2.1]"]]

    for port_i, desc, hwid in sorted(ports_ori):
        name="{}: {} [{}]".format(port_i, desc, hwid)
        txt="{}".format(port_i, desc)
        print("txt: ",txt)
        print("name: ",name)
        L.append(name)

    return (L)

def btncmd():
    global root
    global test
    global port
    global inp

    inp=port.get()

    ports_ori=serial.tools.list_ports.comports()
    # for testing:
    # ports_ori=[["COM1","Arduino Port (COM1)","[ACPI\PNP0501\1]"],["COM7", "MediaTek USB Port (COM7)", "[USB VID:PID=0E8D:0003 SER=6 LOCATION=1-2.1]"]]
    for port_i, desc, hwid in sorted(ports_ori):
        name="{}: {} [{}]".format(port_i, desc, hwid)
        p="{}".format(port_i)
        txt="{}".format(desc)

        if (inp==name):
            if("Arduino" in txt):
                inp=p
                test=True
            else:
                print(txt)
            
    if (test):
        showinfo(
            title='Done',
            message="Arudino's connected on port "+inp
        )
        root.destroy()
        return (inp)
    else:
        showinfo(
            title="Error",
            message="Please choose a correct port"
        )

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

    ttk.Label(frm, text="Select the Arduino's port").grid(column=0, row=0)

    ttk.Label(frm).grid(column=0,row=1) #Separator

    cb=ttk.Combobox(frm,textvariable=port,values=ports(),state="readonly",width=60).grid(column=0, row=2)

    ttk.Label(frm).grid(column=1, row=3) #Separator

    ttk.Button(frm, text="Select",command=btncmd).grid(column=0, row=4)
    ttk.Button(frm, text="Quit", command=root.destroy).grid(column=0, row=5)
    
    root.mainloop()

if __name__=="__main__":
    fn()