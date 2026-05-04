import hashlib
import shutil
import os

# ===== hàm băm SHA-512 =====
def hash_file(path):
    sha512 = hashlib.sha512()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha512.update(chunk)
    return sha512.hexdigest()

# ===== chương trình chính =====
def bai3():
    print("=== MO PHONG GUI - NHAN FILE ===")

    file_path = input("Nhap duong dan file: ")

    if not os.path.exists(file_path):
        print("File khong ton tai!")
        return

    filename = os.path.basename(file_path)
    file_nhan = "nhan_" + filename

    # B1: tính hash ban đầu
    hash_goc = hash_file(file_path)

    # B2: mô phỏng gửi (copy)
    shutil.copy(file_path, file_nhan)

    # B3: tính hash sau khi nhận
    hash_nhan = hash_file(file_nhan)

    # B4: so sánh
    print("\n=== KET QUA ===")
    print("Hash goc:\n", hash_goc)
    print("\nHash nhan:\n", hash_nhan)

    if hash_goc == hash_nhan:
        print("\n=> FILE TOAN VEN (khong bi thay doi)")
    else:
        print("\n=> FILE BI THAY DOI")

# ===== chạy =====
if __name__ == "__main__":
    bai3()