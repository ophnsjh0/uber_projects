import socket
s = socket.socket()
s.settimeout(5)
s.connect(("192.168.74.136", 80))  # IP, Port
print("✅ 연결됨")
