import tkinter as tk
from tkinter import ttk, messagebox
import asyncio, asyncssh
import threading

root = tk.Tk()
root.title("SSH PORT FORWARDING by @n1k1tal0x")
root.geometry("300x500")

tk.Label(text="Choise forward type:").pack()

forward_type = tk.StringVar(value="remote_forward")
tk.Radiobutton(root, text="Remote Forward", variable=forward_type, value="remote_forward").pack()
tk.Radiobutton(root, text="Local Forward", variable=forward_type, value="local_forward").pack()

ttk.Separator(root, orient='horizontal').pack(fill='x')

tk.Label(text="SSH Config:").pack()

tk.Label(text="Ip:").pack()
ssh_ip = tk.Entry(root, width=20)
ssh_ip.pack()

tk.Label(text="Username:").pack()
ssh_username = tk.Entry(root, width=10)
ssh_username.pack()

tk.Label(text="Password:").pack()
ssh_password = tk.Entry(root, width=20)
ssh_password.pack()

ttk.Separator(root, orient='horizontal').pack(fill='x')

tk.Label(text="Remote Config:").pack()

tk.Label(text="Ip:").pack()
remote_ip = tk.Entry(root, width=20, )
remote_ip.pack()

tk.Label(text="Port:").pack()
remote_port = tk.Entry(root, width=10)
remote_port.pack()

ttk.Separator(root, orient='horizontal').pack(fill='x')

tk.Label(text="Local Config:").pack()

tk.Label(text="Ip:").pack()
local_ip = tk.Entry(root, width=20)
local_ip.pack()

tk.Label(text="Port:").pack()
local_port = tk.Entry(root, width=10)
local_port.pack()

ttk.Separator(root, orient='horizontal').pack(fill='x')

async def remote_forward():
    async with asyncssh.connect(ssh_ip.get(), username=ssh_username.get(), password=ssh_password.get()) as conn:
        forwarder = await conn.forward_remote_port(remote_ip.get(), int(remote_port.get()), local_ip.get(), int(local_port.get()))
        try:
            await asyncio.Event().wait()
        finally:
            forwarder.close()

# async def local_forward():
#     async with asyncssh.connect('dcuzya.ru', username='root', password='password') as conn:
#         # Проброс с локального 25565 на dcuzya.ru:25565
#         forwarder = await conn.forward_local_port('127.0.0.1', 25565, '127.0.0.1', 25565)
#         print('Local port forwarding started: 127.0.0.1:25565 → dcuzya.ru:25565')
#         await asyncio.Event().wait()  # Ждём бесконечно (Ctrl+C чтобы остановить)
#         forwarder.close()

def connect():
    if not ssh_ip.get():
        messagebox.showerror("Error", "SSH Config->Ip is empty!")
        return
    if not ssh_username.get():
        messagebox.showerror("Error", "SSH Config->Port is empty!")
        return
    if not ssh_password.get():
        messagebox.showerror("Error", "SSH Config->Password is empty!")
        return
    if not remote_ip.get():
        messagebox.showerror("Error", "Remote Config->Ip is empty!")
        return
    if not remote_port.get():
        messagebox.showerror("Error", "Remote Config->Port is empty!")
        return
    if not local_ip.get():
        messagebox.showerror("Error", "Local Config->Ip is empty!")
        return
    if not local_port.get():
        messagebox.showerror("Error", "Local Config->Port is empty!")
        return
    
    if forward_type.get() == "remote_forward":
        threading.Thread(target=lambda: asyncio.run(remote_forward()), daemon=True).start()
        messagebox.showinfo("Forwarding", "Forward was complited!\nInfo: Close app for stop forwards!")
    else:
        messagebox.showerror("Error", "\"Local Forward\" in dev!")

def faq():
    messagebox.showerror("Error", "\"F.A.Q.\" in dev!")

tk.Button(text="FORWARD", command=connect).pack()
tk.Button(text="F.A.Q.", command=faq).pack()

local_ip.insert(0, "127.0.0.1")
local_port.insert(0, "25565")
remote_ip.insert(0, "0.0.0.0")
remote_port.insert(0, "25565")

root.mainloop()