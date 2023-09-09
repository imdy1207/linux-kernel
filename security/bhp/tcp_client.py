import socket
HOST = '192.168.45.72'
PORT = 9998
#소켓 객체 생성
"""
AF_INET : 표준 IPv4 주소 또는 호스트 이름을 사용
SOCK_STREAM : TCP 클라이언트를 생성
"""
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#클라이언트 연결
client.connect((HOST, PORT))
#임의의 데이터 송신
client.send(b'GET / HTTP/1.1\r\nHOST: google.com\r\n\r\n')
#응답 데이터 수신
response = client.recv(4096)
print(response.decode('utf-8'))
client.close()
