import json
from time import ctime
import threading
import tkinter as tk
from client import Client

with open("settings.json", "r") as settings_file:
    settings = json.load(settings_file)
logbox_count = 0
chatbox_count = 0

def connect_init():
    listbox_msg(logbox, "preparing for connection with server...")
    SERVER = host.get()
    PORT = int(port.get())
    host.delete(0, tk.END)
    port.delete(0, tk.END)
    listbox_msg(logbox, "connecting to server...")
    cli.connect(SERVER, PORT)
    listbox_msg(logbox, "connected to server successfully!")
    send.config(state=tk.ACTIVE)
    disconnect.config(state=tk.ACTIVE)
    connect.config(state=tk.DISABLED)
    thread.start()
    listbox_msg(logbox, "listening for messages...")
    listbox_msg(chatbox, f"connected to [{SERVER}:{PORT}] successfully!")

def disconnect_init():
    listbox_msg(logbox, "disconnecting from server...")
    cli.send_message("!disconnect")
    thread.join()
    listbox_msg(logbox, "disconnected succesfully!")
    disconnect.config(state=tk.DISABLED)
    send.config(state=tk.DISABLED)
    connect.config(state=tk.ACTIVE)

def quit_init():
    listbox_msg(logbox, "quitting...")
    if disconnect.cget("state") == "active":
        disconnect_init()
    window.quit()

def send_msg(event):
    msg = message.get()
    message.delete(0, tk.END)
    cli.send_message(msg)

def handle_chatbox(client):
    connected = True
    while connected:
        data = client.get_data()
        if not data:
            continue
        msg = data.decode(client.FORMAT)
        if msg.lower() == client.DC_MSG:
            break
        chatbox.insert(tk.END, msg)
        chatbox.yview(tk.END)

def listbox_msg(listbox, msg):
    listbox.insert(tk.END, f"[{ctime()}]: {msg}")

DC_MSG = settings.get("DC_MSG")
MAX_BYTES = int(settings.get("MAX_BYTES"))
FORMAT = settings.get("FORMAT")

cli = Client(DC_MSG, MAX_BYTES, FORMAT)
thread = threading.Thread(target=handle_chatbox, args=[cli])

label_font = ("Consolas", 20)
console_font = ("Consolas", 13)
logging_font = ("Consolas", 6)

win_x = 1024
win_y = 576
win_padx = 10
win_pady = 10
settings_frame_padx = 20
settings_frame_pady = 30

window = tk.Tk()
window.title("Falcon")
window.iconbitmap("favicon.ico")
window.geometry(f"{win_x}x{win_y}")
window.configure(background="black")

settings_frame = tk.Frame(window, padx=win_padx, pady=win_pady, bg="grey")
settings_frame.grid(row=0, column=0, sticky="EWNS")

config_frame = tk.Frame(settings_frame, padx=settings_frame_padx, pady=settings_frame_pady)
config_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
tk.Label(config_frame, text="Connectives:", font=label_font).pack(side=tk.TOP, fill=tk.NONE)

host_frame = tk.Frame(config_frame)
host_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
tk.Label(host_frame, text="Host :", font=label_font).pack(side=tk.LEFT, fill=tk.NONE)
host = tk.Entry(host_frame, font=label_font)
host.pack(side=tk.LEFT, fill=tk.X, expand=True)

port_frame = tk.Frame(config_frame)
port_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
tk.Label(port_frame, text="Port :", font=label_font).pack(side=tk.LEFT, fill=tk.NONE)
port = tk.Entry(port_frame, font=label_font)
port.pack(side=tk.LEFT, fill=tk.X, expand=True)

group_frame = tk.Frame(config_frame)
group_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
tk.Label(group_frame, text="Group:", font=label_font).pack(side=tk.LEFT, fill=tk.NONE)
group = tk.Entry(group_frame, font=label_font, state=tk.DISABLED)
group.pack(side=tk.LEFT, fill=tk.X, expand=True)

connect_frame = tk.Frame(config_frame)
connect_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
connect = tk.Button(connect_frame, text="Connect", font=label_font, command=connect_init)
connect.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

exit_frame = tk.Frame(config_frame)
exit_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
disconnect = tk.Button(exit_frame, text="Disconnect", font=label_font, state=tk.DISABLED, command=disconnect_init)
disconnect.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
tk.Button(exit_frame, text="Quit", font=label_font, command=quit_init).pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

logs_frame = tk.Frame(settings_frame, padx=settings_frame_padx, pady=settings_frame_pady)
logs_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
tk.Label(logs_frame, text="Logs:", font=label_font).pack(side=tk.TOP, fill=tk.NONE)

logbox_frame = tk.Frame(logs_frame)
logbox_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
logbox = tk.Listbox(logbox_frame, font=logging_font)
logbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

chatting_frame = tk.Frame(window, padx=win_padx, pady=win_pady, bg="grey")
chatting_frame.grid(row=0, column=1, sticky="EWNS")
tk.Label(chatting_frame, text="Chat:", font=label_font).pack(side=tk.TOP, fill=tk.X)

chatbox_frame = tk.Frame(chatting_frame, padx=settings_frame_padx, pady=settings_frame_pady)
chatbox_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
chatbox = tk.Listbox(chatbox_frame, font=console_font)
chatbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

message_frame = tk.Frame(chatbox_frame, pady=20)
message_frame.pack(side=tk.TOP, fill=tk.X)
message = tk.Entry(message_frame, font=label_font, relief=tk.RAISED)
message.pack(side=tk.LEFT, fill=tk.X, expand=True)
message.bind("<Return>", send_msg)
send = tk.Button(message_frame, text="send", font=console_font, state=tk.DISABLED, command=send_msg)
send.pack(side=tk.LEFT, fill=tk.NONE)

window.columnconfigure(1, weight=1)
window.rowconfigure(0, weight=1)

window.protocol("WM_DELETE_WINDOW", quit_init)
window.mainloop()
