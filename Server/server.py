from threading import Thread
import socket
from tkinter import *
import tkinter as tk
import program

SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind((socket.gethostbyname(socket.gethostname()), 5050))
print("server is working on ", (socket.gethostbyname(socket.gethostname())))

SERVER.listen()

def waitingConnection():
    print("Waiting for Client")
    while True:
        client, Address = SERVER.accept()
        print("Client", Address, "connected!")
        Thread(target=program.takeRequest, args=(client,)).start()

def action():
    try:
        SERVER.listen()
        ACCEPT_THREAD = Thread(target=waitingConnection)
        ACCEPT_THREAD.start()
        ACCEPT_THREAD.join()
    except:
        print("Error occurred!")
    finally:
        SERVER.close()

def main():
    top = Tk()
    top.title("Server")
    top.geometry("300x200")
    top.configure(bg="#FDF4F5")
    imageActive = tk.PhotoImage(file='./images/active.png')
    top.button = tk.Button(top, text="Activate Server", font=('Helvetica Bold', 11),image=imageActive, command=action, bd=10, bg="#93BFCF", fg="black", activebackground='#6096B4', activeforeground='white')
    top.button.pack(fill=BOTH, pady=10, padx=10, expand=True)
    top.mainloop()

if __name__ == "__main__":
    main()
