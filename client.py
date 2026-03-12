import socket
import threading
import tkinter as tk
from tkinter import simpledialog

HOST = "127.0.0.1"
PORT = 4100

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

root = tk.Tk()
root.withdraw()

username = simpledialog.askstring("Username", "Enter your username")

chat_window = tk.Toplevel(root)
chat_window.title("Chat Client")

chat_box = tk.Text(chat_window, height=20, width=50)
chat_box.pack()

msg_entry = tk.Entry(chat_window, width=50)
msg_entry.pack()

# OSI Layer logging for sending
def log_osi_layers_send_client(message):
    print("\n--- Sending Message Through OSI Layers ---")
    print(f"[Application Layer] Composing: {message}")
    print("[Presentation Layer] Encoding to bytes")
    print("[Session Layer] Maintaining session with server")
    print("[Transport Layer] Sending via TCP")
    print("[Network Layer] Server IP checked")
    print("[Data Link Layer] Frame created")
    print("[Physical Layer] Signal transmitted\n")

# OSI Layer logging for receiving
def log_osi_layers_receive_client(message):
    print("\n--- Receiving Message Through OSI Layers ---")
    print("[Physical Layer] Signal received")
    print("[Data Link Layer] Frame received and checked")
    print("[Network Layer] IP and port verified")
    print("[Transport Layer] TCP segment received")
    print("[Session Layer] Session active")
    print("[Presentation Layer] Decoding bytes to text")
    print(f"[Application Layer] Message: {message}\n")

def receive():
    while True:
        try:
            message = client.recv(1024).decode()
            if message == "USERNAME":
                client.send(username.encode())
            else:
                log_osi_layers_receive_client(message)
                chat_box.insert(tk.END, message + "\n")
                chat_box.see(tk.END)
        except:
            chat_box.insert(tk.END, "Connection lost.\n")
            break

def send_message(event=None):
    message = msg_entry.get()
    if message.strip() != "":
        full_message = f"{username}: {message}"
        log_osi_layers_send_client(full_message)
        client.send(full_message.encode())
    msg_entry.delete(0, tk.END)

send_btn = tk.Button(chat_window, text="Send", command=send_message)
send_btn.pack()

msg_entry.bind("<Return>", send_message)

receive_thread = threading.Thread(target=receive)
receive_thread.daemon = True
receive_thread.start()

root.mainloop()