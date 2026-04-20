import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime

from des_socket_utils import (
    HEADER_SIZE, parse_header, recv_exact,
    decrypt_des_cbc, encrypt_des_cbc, build_packet
)

HOST = '0.0.0.0'   # CHO PHÉP NHẬN TỪ MÁY KHÁC
PORT = 6000

client_socket = None

# ================= GUI =================
root = tk.Tk()
root.title(" Secure DES Chat Pro")
root.geometry("650x550")
root.configure(bg="#0f172a")

# ===== STYLE =====
BG = "#0f172a"
CHAT_BG = "#020617"
FG = "#e2e8f0"
ACCENT = "#38bdf8"

# ===== TITLE =====
title = tk.Label(root, text=" SECURE CHAT", font=("Segoe UI", 18, "bold"),
                 bg=BG, fg=ACCENT)
title.pack(pady=10)

# ===== CHAT BOX =====
chat_box = scrolledtext.ScrolledText(
    root,
    bg=CHAT_BG,
    fg=FG,
    font=("Consolas", 10),
    insertbackground="white",
    bd=0
)
chat_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

def log(msg, sender="SYS"):
    time = datetime.now().strftime("%H:%M:%S")
    chat_box.insert(tk.END, f"[{time}] {sender}: {msg}\n")
    chat_box.see(tk.END)

# ===== INPUT =====
frame = tk.Frame(root, bg=BG)
frame.pack(pady=5)

entry = tk.Entry(frame, width=40, bg="#1e293b", fg="white",
                 insertbackground="white", bd=0, font=("Segoe UI", 11))
entry.grid(row=0, column=0, padx=5, ipady=6)

# ===== BUTTON =====
def btn(text, cmd):
    return tk.Button(frame, text=text, command=cmd,
                     bg=ACCENT, fg="black",
                     font=("Segoe UI", 10, "bold"),
                     bd=0, padx=10)

# ================= SERVER =================
def handle_client(conn):
    global client_socket
    client_socket = conn

    while True:
        try:
            header = recv_exact(conn, HEADER_SIZE)
            if not header:
                break

            key, iv, length = parse_header(header)
            cipher_bytes = recv_exact(conn, length)

            plaintext = decrypt_des_cbc(key, iv, cipher_bytes)
            msg = plaintext.decode()

            log(msg, "PEER")

        except:
            break

def start_server():
    def server_thread():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            log(f"Listening on {PORT}")

            conn, addr = s.accept()
            log(f"Connected from {addr}")

            threading.Thread(target=handle_client, args=(conn,), daemon=True).start()

    threading.Thread(target=server_thread, daemon=True).start()

# ================= CLIENT =================
def connect_to_server():
    global client_socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ip = entry.get()

        s.connect((ip, PORT))
        client_socket = s

        log(f"Connected to {ip}")
        threading.Thread(target=handle_client, args=(s,), daemon=True).start()

    except Exception as e:
        log(f"Connect error: {e}")

# ================= SEND =================
def send_message():
    global client_socket

    if not client_socket:
        log("Not connected!")
        return

    msg = entry.get()
    if not msg:
        return

    plain = msg.encode()
    key, iv, cipher = encrypt_des_cbc(plain)
    packet = build_packet(key, iv, cipher)

    try:
        client_socket.sendall(packet)
        log(msg, "ME")
        entry.delete(0, tk.END)
    except Exception as e:
        log(f"Send error: {e}")

# ===== BUTTONS =====
btn("Start Server", start_server).grid(row=0, column=1, padx=5)
btn("Connect", connect_to_server).grid(row=0, column=2, padx=5)
btn("Send", send_message).grid(row=0, column=3, padx=5)

# ===== ENTER KEY =====
entry.bind("<Return>", lambda e: send_message())

root.mainloop()     