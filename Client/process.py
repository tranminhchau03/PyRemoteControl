# process.py
import tkinter as tk
from tkinter import messagebox, ttk

def process_running(self, client):
    try:
        self.process = tk.Tk()
        self.process.configure(bg = "#FFFAF0")
        self.process.title("Process Running")
        #clear task
        def DelTask():
            self.frame_process.destroy()

        def SeeTask():
            global frame_process
            self.length = 0
            self.ID = [''] * 100000
            self.Name = [''] * 100000
            self.Thread = [''] * 100000
            try:
                client.sendall(bytes("ProcessRunning","utf-8"))
            except:
                messagebox.showinfo("!Warning", "Lỗi kết nối ")
                self.process.destroy()

            #Receive data
            try:
                self.length = int(client.recv(1024).decode("utf-8"))
                for i in range(self.length):
                    self.ID[i] = client.recv(1024).decode("utf-8")
                    client.sendall(bytes(self.ID[i], "utf-8"))
                for i in range(self.length):
                    self.Name[i] = client.recv(1024).decode("utf-8")
                    client.sendall(bytes(self.Name[i], "utf-8"))
                for i in range(self.length):
                    self.Thread[i] = client.recv(1024).decode("utf-8")
                    client.sendall(bytes(self.Thread[i], "utf-8"))
            except:
                messagebox.showinfo("!Warning", "Lỗi kết nối ")

            self.frame_process = tk.Frame(self.process, bg = "white",padx=20, pady = 20, borderwidth=5)
            self.frame_process.grid(row=1,columnspan=5,padx=20)

            self.scrollbar = tk.Scrollbar(self.frame_process)
            self.scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
            self.mybar = ttk.Treeview(self.frame_process, yscrollcommand=self.scrollbar.set)
            self.mybar.pack()
            self.scrollbar.config(command=self.mybar.yview)

            self.mybar['columns'] = ("1","2") 
            self.mybar.column("#0", anchor=tk.CENTER, width =200,minwidth=25)
            self.mybar.column("1", anchor=tk.CENTER, width=100)
            self.mybar.column("2", anchor=tk.CENTER, width=100)

            self.mybar.heading("#0", text="Process Name", anchor=tk.W)
            self.mybar.heading("1",text = "ID", anchor=tk.CENTER)
            self.mybar.heading("2", text = "Counting threading", anchor=tk.CENTER)
            for i in range(self.length):
                self.mybar.insert(parent='', index='end',iid=0+i, text = self.Name[i], values=(self.ID[i],self.Thread[i]))
        #kill screen
        def KillWindow():
            self.KillTask = tk.Tk()
            self.KillTask.geometry("400x50")
            self.KillTask.title("Kill")
            self.EnterName = tk.Entry(self.KillTask, width = 35)
            self.EnterName.grid(row=0, column=0, columnspan = 3, padx = 5, pady = 5 )
            self.EnterName.insert(tk.END,"Nhập Process ID")
            def PressKill1():
                self.AppName = self.EnterName.get()
                client.sendall(bytes("KillTask","utf-8"))
                try:
                    
                    client.sendall(bytes(self.AppName,"utf-8"))
                    self.checkdata = client.recv(1024).decode("utf-8")
                    messagebox.showinfo("", "Đã diệt chương trình")
                except:
                    messagebox.showinfo("", "Không tìm thấy chương trình")

            KillButton = tk.Button(self.KillTask, bg = "#FFE4E1",text = "Kill", font = "Helvetica 9 bold", padx = 20, command = PressKill1, bd = 5, activebackground='#F4A460').grid(row=0, column=4, padx=5, pady=5)
        #start window
        def StartTask():
            self.StartTask = tk.Tk()
            self.StartTask.geometry("300x50")
            self.StartTask.title("Start")

            self.EnterName = tk.Entry(self.StartTask, width = 35)
            self.EnterName.grid(row = 0, column = 0, columnspan = 3, padx = 5, pady = 5)
            self.EnterName.insert(tk.END,"Nhập Tên")

            def PressStart1():
                self.Name = self.EnterName.get()
                client.sendall(bytes("OpenTask","utf-8"))
                try:
                    client.sendall(bytes(self.Name,"utf-8"))
                    self.checkdata = client.recv(1024).decode("utf-8")
                    messagebox.showinfo("", "Chương trình đã bật")
                except:
                    messagebox.showinfo("", "Không tìm thấy chương trình")

            StartButton = tk.Button(self.StartTask, text = "Start", bg = "#FFE4E1",font = "Helvetica 9 bold", padx = 20, command = PressStart1).grid(row=0, column=4, padx=5, pady=5)

        Kill = tk.Button( self.process, text = "Kill", bg='#FFE5E5',font = "Helvetica 9 bold", padx = 30,  pady = 20, command= KillWindow, bd = 5, activebackground='#FFBFBF').grid(row = 0, column = 0, padx = 0)
        Watch = tk.Button(self.process, text = "See more", bg='#FFE5E5', font = "Helvetica 9 bold",  padx = 30,  pady = 20, command = SeeTask, bd = 5, activebackground='#FFBFBF').grid(row = 0, column = 1, padx = 0)
        Delete = tk.Button(self.process, text =  "See less", bg='#FFE5E5',font = "Helvetica 9 bold", padx = 30, pady = 20, command = DelTask, bd = 5, activebackground='#FFBFBF').grid(row = 0, column = 2, padx = 0)
        Start = tk.Button(self.process, text="Start", bg='#FFE5E5', font = "Helvetica 9 bold", padx = 30, pady = 20, command = StartTask, bd = 5, activebackground='#FFBFBF').grid(row = 0, column = 3, padx = 0)

    except:
        messagebox.showinfo("!Warning", "Lỗi kết nối ")
