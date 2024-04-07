# app.py
import tkinter as tk
from tkinter import messagebox, ttk

def app_running(self, client):
    self.app = tk.Tk()
    self.app.title("App Running")
    self.app.configure (bg = "white")
    #clear app list
    def DelTask():
        self.frame_app.destroy()
    #see app list
    def SeeTask():
        global frame_app
        global PORT
        PORT = 5656
        self.length = 0 #Danh sách các app đang chạy
        self.ID = [''] * 100 #Mảng lưu ID của app
        self.Name = [''] * 100 #Lưu tên app
        self.Thread = [''] * 100 #lưu luồng
        try:
            client.sendall(bytes("AppRunning","utf-8"))
        except:
            messagebox.showinfo("Warning!", "Lỗi kết nối ")
            self.app.destroy()
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
            box = messagebox.showinfo("!Warning", "Lỗi kết nối ")

        self.frame_app = tk.Frame(self.app, bg = "#FDF4F5", padx=20, pady = 20, borderwidth=5)
        self.frame_app.grid(row=1,columnspan=5,padx=20)
        

        self.scrollbar = tk.Scrollbar(self.frame_app)
        self.scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
        self.mybar = ttk.Treeview(self.frame_app, yscrollcommand=self.scrollbar.set)
        self.mybar.pack()
        self.scrollbar.config(command=self.mybar.yview)

        self.mybar['columns'] = ("1","2") 
        self.mybar.column("#0", anchor=tk.CENTER, width =200,minwidth=25)
        self.mybar.column("1", anchor=tk.CENTER, width=100)
        self.mybar.column("2", anchor=tk.CENTER, width=100)

        self.mybar.heading("#0", text="App Name", anchor=tk.W)
        self.mybar.heading("1",text = "ID", anchor=tk.CENTER)
        self.mybar.heading("2", text = "Counting threading", anchor=tk.CENTER)
        for i in range(self.length):
            self.mybar.insert(parent='', index='end',iid=0+i, text = self.Name[i], values=(self.ID[i],self.Thread[i]))
    #kill screen
    def KillWindow():
        self.KillTask = tk.Tk()
        self.KillTask.geometry("500x50")
        self.KillTask.title("Kill")
        self.EnterName = tk.Entry(self.KillTask, width = 35)
        self.EnterName.grid(row=0, column=0, columnspan = 3, padx = 5, pady = 5 )
        self.EnterName.insert(tk.END,"Nhập tên")

        def PressKill():
            self.AppName = self.EnterName.get()
            client.sendall(bytes("KillApp","utf-8"))
            try:
                client.sendall(bytes(self.AppName,"utf-8"))
                self.checkdata = client.recv(1024).decode("utf-8")
                if (self.checkdata == "Da xoa tac vu"):
                    messagebox.showinfo("", "Đã diệt chương trình")
                else:
                    messagebox.showinfo("", "Không tìm thấy chương trình")
            except:
                messagebox.showinfo("", "Không tìm thấy chương trình")

        KillButton = tk.Button(self.KillTask, text = "Kill", bg = "#C6C6E2",font = "Helvetica 9 bold",padx = 20, command = PressKill, bd = 5, activebackground='#F4A460').grid(row=0, column=4, padx=5, pady=5)
    #start screen
    def StartTask():
        self.StartTask = tk.Tk()
        self.StartTask.geometry("500x50")
        self.StartTask.title("Start")

        self.EnterName = tk.Entry(self.StartTask, width = 35)
        self.EnterName.grid(row = 0, column = 0, columnspan = 3, padx = 5, pady = 5)
        self.EnterName.insert(tk.END,"Nhập Tên")

        def PressStart():
            self.Name = self.EnterName.get()
            client.sendall(bytes("OpenTask","utf-8"))
            try:
                client.sendall(bytes(self.Name,"utf-8"))
                self.checkdata = client.recv(1024).decode("utf-8")
                if (self.checkdata == "Da mo"):
                    messagebox.showinfo("", "Chương trình đã bật")
            except:
                messagebox.showinfo("", "Không tìm thấy chương trình")

        StartButton = tk.Button(self.StartTask, text = "Start",bg = "#C6C6E2",font = "Helvetica 9 bold", padx = 20, command = PressStart, bd = 5, activebackground='#F4A460').grid(row=0, column=4, padx=5, pady=5)

    Kill = tk.Button( self.app, text = "Kill",bg = "#C6C6E2",font = "Helvetica 9 bold", padx = 30,  pady = 20, command= KillWindow, bd = 5, activebackground='#FFFFA5').grid(row = 0, column = 0, padx = 10)
    Watch = tk.Button(self.app, text = "See more",bg = "#C6C6E2",font = "Helvetica 9 bold", padx = 30,  pady = 20, command = SeeTask, bd = 5, activebackground='#FFFFA5').grid(row = 0, column = 1, padx = 10)
    Delete = tk.Button(self.app, text =  "See less",bg = "#C6C6E2", font = "Helvetica 9 bold",padx = 30, pady = 20, command = DelTask, bd = 5, activebackground='#FFFFA5').grid(row = 0, column = 2, padx = 10)
    Start = tk.Button(self.app, text="Start", bg = "#C6C6E2", font = "Helvetica 9 bold",padx = 30, pady = 20, command = StartTask, bd = 5, activebackground='#F4A460').grid(row = 0, column = 3, padx = 10)
