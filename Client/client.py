# client.py
import tkinter as tk
from tkinter import messagebox, ttk, filedialog, PhotoImage
from PIL import ImageTk, Image
import io
from threading import Thread
from socket import AF_INET, socket, SOCK_STREAM
import takepic
import process
import keylog
import app

class GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.withdraw()
        self.window.configure(bg="#F5F5F5")
        self.login = tk.Toplevel()
        self.login.configure(bg="#F5F5F5")
        self.login.title("User")
        self.login.resizable(width=False, height=False)
        self.login.geometry("600x300")

        # Load images for buttons
        self.image_process = tk.PhotoImage(file="./images/process.png")
        self.image_app = tk.PhotoImage(file="./images/app.png")
        self.image_capture = tk.PhotoImage(file="./images/capture.png")
        self.image_shutdown = tk.PhotoImage(file="./images/shutdown.png")
        self.image_key = tk.PhotoImage(file="./images/keystroke.png")
        
        self.pls = tk.Label(self.login, text="Nhập địa chỉ IP:", bg="#F5F5F5", font="Helvetica 14 bold")
        self.pls.place(relheight=0.15, relx=0.4, rely=0.07)

        Id = tk.StringVar()
        
        # Use ttk.Entry to create a themed Entry widget
        self.entryName = ttk.Entry(self.login, textvariable=Id, font=("Helvetica", 10), style="Rounded.TEntry")
        
        # Create a custom style for rounded border Entry
        self.login.style = ttk.Style()
        self.login.style.configure("Rounded.TEntry", borderwidth=5, relief="ridge", padding=(10, 5), bordercolor="blue", background="white")
        
        self.entryName.place(relwidth=0.6, relheight=0.1, relx=0.2, rely=0.4)  # Adjust the size and position
        self.entryName.focus()

        imageConnect = tk.PhotoImage(file="./images/connect.png")
        self.go = tk.Button(self.login, text="Kết nối!", bg="#F5F5F5", font="Helvetica 20 bold", image=imageConnect, height=60, width=180,
                            command=lambda: self.ConnectServer(self.entryName.get()), bd=5, activebackground='grey')
        self.go.place(relx=0.35, rely=0.55)
        self.go.image = imageConnect

    #function to turn off window
    def shutdown(self, client):
        try:
            client.sendall(bytes("Shutdown", 'utf-8'))
        except:
            messagebox.showinfo("", "Lỗi kết nối ")

    def takepicture(self, client):
        takepic.take_picture(self, client)

    def processrunning(self, client):
        process.process_running(self, client)

    def apprunning(self, client):
        app.app_running(self, client)

    def keystroke(self, client):
        keylog.key_stroke(self, client)

    def control(self, client):
        self.top = tk.Toplevel()  # Use Toplevel instead of Tk
        self.top.configure(bg="#FDF4F5")

        window_width = 600
        window_height = 300
        self.top.geometry(f"{window_width}x{window_height}")
        self.top.title("Control")

        button_params = {
            'font': ('Arial 10 bold'),
            'bd': 5,
            'activebackground': '#C4C1A4',
        }

        self.process = tk.Button(
            self.top,
            text="Process Running",
            height=290,
            width=110,
            image=self.image_process,
            bg='#EEE0C9',
            fg='black',
            command=lambda: self.processrunning(client),
            **button_params
        )
        self.process.image = self.image_process
        self.process.grid(row=1, column=0, rowspan=4)

        self.app = tk.Button(
            self.top,
            text="App Running",
            width=300,
            height=50,
            image=self.image_app,
            bg='#EEE0C9',
            fg='black',
            command=lambda: self.apprunning(client),
            **button_params
        )
        self.app.image = self.image_app
        self.app.grid(row=1, column=1, columnspan=2)

        self.shut = tk.Button(
            self.top,
            text="Shutdown",
            width=100,
            height=5,
            image=self.image_shutdown,
            bg='#DFCCFB',
            fg='black',
            command=lambda: self.shutdown(client),
            **button_params
        )
        self.shut.image = self.image_shutdown
        self.shut.grid(row=2, column=1, columnspan=1, rowspan=2, sticky="nsew")

        self.capture = tk.Button(
            self.top,
            text="Screenshot",
            width=100,
            height=5,
            image=self.image_capture,
            bg='#DFCCFB',
            fg='black',
            command=lambda: self.takepicture(client),
            **button_params
        )
        self.capture.image = self.image_capture
        self.capture.grid(row=2, column=2, columnspan=1, rowspan=2, sticky="nsew")

        self.key = tk.Button(
            self.top,
            text="Keystroke",
            height=220,
            width=100,
            image=self.image_key,
            bg='#EEE0C9',
            fg='black',
            command=lambda: self.keystroke(client),
            **button_params
        )
        self.key.image = self.image_key
        self.key.grid(row=1, column=4, rowspan=3, columnspan=2)

        self.escape = tk.Button(self.top, text="Quit", width=11, bg='#EEE0C9', fg='black', command=lambda: self.exist(client), **button_params)
        self.escape.grid(row=4, column=4)
        
        self.top.grid_rowconfigure(0, weight=1)
        self.top.grid_rowconfigure(1, weight=1)
        self.top.grid_rowconfigure(2, weight=1)
        self.top.grid_rowconfigure(3, weight=1)
        self.top.grid_rowconfigure(4, weight=1)
        self.top.grid_columnconfigure(0, weight=1)
        self.top.grid_columnconfigure(1, weight=1)
        self.top.grid_columnconfigure(2, weight=1)
        self.top.grid_columnconfigure(3, weight=1)
        self.top.grid_columnconfigure(4, weight=1)
        self.top.grid_columnconfigure(5, weight=1)
        self.top.grid_columnconfigure(6, weight=1)

        # self.top.mainloop()


    def run(self):
        self.login.mainloop()

    def exist(self, client):
        client.close()
        self.top.destroy()

    def receive(self, client):
        try:
            messagebox.showinfo("Kết nối!", "Kết nối đến server thành công")
            self.login.destroy()
            rcv = Thread(target=self.control, args=(client,))
            rcv.start()
        except Exception as e:
            print("!ERROR:", e)
            client.close()

    def ConnectServer(self, HOST):
        client = socket(AF_INET, SOCK_STREAM)
        try:
            client.connect((HOST, 5050))
            client.send(bytes("Thành công", 'utf-8'))
            rcv = Thread(target=self.receive, args=(client,))
            rcv.start()
        except Exception as e:
            messagebox.showinfo(" !ERROR ", "Chưa kết nối đến server: " + str(e))

def main():
    gui = GUI()
    gui.run()

if __name__ == "__main__":
    main()
