import hashlib
import os

def hash_file(path):
    sha512 = hashlib.sha512()
    
    with open(path, "rb") as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            sha512.update(data)
    
    return sha512.digest()

# Nhập 2 ảnh để so sánh
file1 = input("Nhap duong dan anh thu 1: ")
file2 = input("Nhap duong dan anh thu 2: ")

# Kiểm tra file tồn tại
if not os.path.exists(file1):
    print("Anh 1 khong ton tai")
    exit()

if not os.path.exists(file2):
    print("Anh 2 khong ton tai")
    exit()

# Tính hash và so sánh
if hash_file(file1) == hash_file(file2):
    print("Hai anh giong nhau (khong bi thay doi)")
else:
    print("Hai anh khac nhau (da bi thay doi)")