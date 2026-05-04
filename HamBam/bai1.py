import hashlib

def hash_data(data):
    data_bytes = data.encode('utf-8')
    sha256 = hashlib.sha256(data_bytes).hexdigest()
    sha512 = hashlib.sha512(data_bytes).hexdigest()
    return sha256, sha512

# Nhập dữ liệu ban đầu
data1 = input("Nhập dữ liệu ban đầu: ")

h1_256, h1_512 = hash_data(data1)

print("\n--- Hash ban đầu ---")
print("SHA-256:", h1_256)
print("SHA-512:", h1_512)

# Nhập dữ liệu sau khi sửa
data2 = input("\nNhập dữ liệu sau khi sửa: ")

h2_256, h2_512 = hash_data(data2)

print("\n--- Hash sau khi sửa ---")
print("SHA-256:", h2_256)
print("SHA-512:", h2_512)

# So sánh
print("\n--- So sánh ---")
if h1_256 == h2_256:
    print("SHA-256: KHÔNG đổi")
else:
    print("SHA-256: ĐÃ thay đổi")

if h1_512 == h2_512:
    print("SHA-512: KHÔNG đổi")
else:
    print("SHA-512: ĐÃ thay đổi")