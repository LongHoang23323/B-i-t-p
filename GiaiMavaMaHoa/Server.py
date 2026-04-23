import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# Cấu hình mạng
HOST = '0.0.0.0'
DATA_PORT = 5000
KEY_PORT = 5001

class ServerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AES Decryption Server")
        self.root.geometry("500x400")

        # Thành phần giao diện
        self.label = tk.Label(root, text="Trạng thái hệ thống:", font=("Arial", 10, "bold"))
        self.label.pack(pady=5)

        self.log_area = scrolledtext.ScrolledText(root, width=60, height=15, state='disabled')
        self.log_area.pack(padx=10, pady=5)

        self.start_button = tk.Button(root, text="Khởi động Server", command=self.run_server_thread, bg="green", fg="white")
        self.start_button.pack(pady=10)

    def log(self, message):
        """Hàm cập nhật log lên giao diện"""
        self.log_area.configure(state='normal')
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.configure(state='disabled')
        self.log_area.see(tk.END)

    def run_server_thread(self):
        """Chạy server trong một luồng riêng để không làm treo giao diện"""
        self.start_button.config(state='disabled')
        thread = threading.Thread(target=self.start_server, daemon=True)
        thread.start()

    def start_server(self):
        try:
            # --- Nhận AES key và IV ---
            key_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            key_socket.bind((HOST, KEY_PORT))
            key_socket.listen(1)
            self.log(f"[*] Đang đợi Key/IV tại cổng {KEY_PORT}...")
            
            key_conn, _ = key_socket.accept()
            aes_key = key_conn.recv(16) 
            iv = key_conn.recv(16)
            self.log("[+] Đã nhận Key và IV thành công.")
            key_conn.close()
            key_socket.close()

            # --- Nhận và giải mã dữ liệu ---
            data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            data_socket.bind((HOST, DATA_PORT))
            data_socket.listen(1)
            self.log(f"[*] Đang đợi dữ liệu tại cổng {DATA_PORT}...")
            
            data_conn, _ = data_socket.accept()
            header = data_conn.recv(4)
            if not header:
                return
            
            data_len = int.from_bytes(header, byteorder='big')
            ciphertext = b""
            while len(ciphertext) < data_len:
                chunk = data_conn.recv(4096)
                if not chunk: break
                ciphertext += chunk

            # Giải mã
            cipher = AES.new(aes_key, AES.MODE_CBC, iv=iv)
            try:
                decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)
                self.log(f"\n[DỮ LIỆU NHẬN ĐƯỢC]:\n{decrypted_data.decode('utf-8')}")
            except Exception as e:
                self.log(f"[-] Lỗi giải mã: {e}")

            data_conn.close()
            data_socket.close()
            self.log("\n[!] Kết nối đã đóng. Nhấn nút để khởi động lại.")
            self.start_button.config(state='normal')

        except Exception as e:
            self.log(f"[-] Lỗi hệ thống: {e}")
            self.start_button.config(state='normal')

if __name__ == "__main__":
    root = tk.Tk()
    app = ServerGUI(root)
    root.mainloop()