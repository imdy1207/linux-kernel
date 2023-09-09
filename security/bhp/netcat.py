import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading

'''
1~7 : 필요한 라이브러리들을 첨부
execute : 명령어를 입력받아 실행한 후 결괏값을 화면에 문자열로 출력하는 함수
subprocess 라이브러리 : 프로세스 생성에 인터페이스를 제공하는 강력한 방법 
    -> 클라이언트 프로그램과 통신할 때 다양한 방법을 제공
'''
def execute(cmd):
    cmd = cmd.strip()
    if not cmd:
        return
    output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
    #check_output : 대상 운영체제에서 명령어를 수행한 후 그 결괏값을 반환

    return output.decode()

class NetCat:
    # NetCat 객체 초기화
    def __init__(self, args, buffer=None):
        self.args = args
        self.buffer = buffer # 커맨드 라인 입력으로 전달된 매개변수와 버퍼 내용을 객체에 할당
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # 소켓 객체 생성
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    def run(self): # run() 함수 구현, NetCat 객체의 실행을 처리하는 엔트리 포인트 역할
        if self.args.listen: # 수신 측에서 사용하는 경우 listen() 함수 호출
            self.listen()
        else: # 송신 측이라면 send() 함수 호출
            self.send()
    def send(self):
        self.socket.connect((self.args.target, self.args.port)) # 송신을 위해 먼저 대상의 IP 주소 및 포트 번호를 이용해 연결을 수립
        if self.buffer: # 기존에 버퍼에 저장하고 있는 내용이 있다면 우선 해당 내용을 전송
            self.socket.send(self.buffer)
        try: # 중간에 연결을 종료하고 싶다면 CTRL-C를 눌러 수동으로 끊을 수 있다.
            while True: # 대상으로부터 데이터를 수신
                recv_len = 1
                response = ''
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()
                    if recv_len < 4096:
                        break # 대상으로부터 받은 데이터가 없다면 반복문 탈출
                if response: # 데이터가 있다면
                    print(response) # 해당 내용을 출력
                    buffer = input('> ') # 일시 정지해 입력 받을 수 있도록 한다.
                    buffer += '\n'
                    self.socket.send(buffer.encode()) # 입력된 내용은 대상에게 전송한다.
            # 반복문을 통해 지속 수행
        except KeyboardInterrupt: # CTRL-C가 발생하면 종료
            print('User terminated.')
            self.socket.close() # 소켓도 닫힘
            sys.exit()
    def listen(self):
        print('listening')
        self.socket.bind((self.args.target, self.args.port)) # 지정된 IP와 포트 번호를 통해 bind를 먼저 수행
        self.socket.listen(5)
        while True: # 수신을 대기
            client_socket, _ = self.socket.accept() # 연결되는 소켓이 발생하면
            client_thread = threading.Thread(target=self.handle, args=(client_socket,)) # 연결된 소켓을 handle() 함수로 전달
            client_thread.start()
    def handle(self, client_socket): # 주어진 커맨드 라인 매개변수들의 작업을 각각 알맞게 실행하는 역할
        #명령어 수행, 파일 업로드 또는 셸 실행 등의 작업에 해당된다.
        if self.args.execute: # 명령어 실행
            output = execute(self.args.execute) # 수행하려는 명령어를 execute() 함수로 전달
            client_socket.send(output.encode()) # 그 결괏값을 다시 소켓에 되돌려 보낸다.
        elif self.args.upload: # 파일 업로드 수행
            file_buffer = b''
            while True: # 파일 내용 수신
                data = client_socket.recv(4096)
                if data:
                    file_buffer += data
                    print(len(file_buffer))
                else: # 더 이상 수신할 데이터가 없으면
                    break
            with open(self.args.upload, 'wb') as f:
                f.write(file_buffer) # 수신한 내용을 합산해 특정 파일 형태로 기록
            messages = f'Saved file {self.args.upload}'
            client_socket.send(messages.encode())
        elif self.args.command: # 셸을 생성하는 경우
            cmd_buffer = b''
            while True:
                try:
                    client_socket.send(b' #> ') # 송신 측에게 명령어 프롬프트를 전달
                    while '\n' not in cmd_buffer.decode(): # 명령어 문자열이 도착할 때까지 대기
                        cmd_buffer += client_socket.recv(64)
                    print(cmd_buffer)
                    response = execute(cmd_buffer.decode()) # 전달된 명령어 실행에는 execute() 함수를 사용하고
                    if response:
                        client_socket.send(response.encode()) # 해당 명령어의 수행 결괏값을 송신 측에 응답
                    cmd_buffer = b''
                    # 개행 문자가 있는지를 검사해 해당 명령어의 처리 시점을 결정
                    #   -> NetCat과 유사하게 동작하도록 한 것
                    #   -> 이 프로그램은 수신 측에서 동작시키고, 송신 측에서는 원래의 NetCat을 사용해도 좋다.
                    # 하지만 만약 클라이언트 측이 파이썬 프로그램으로 동작하려 한다면 다시 개행 문자를 추가
                except Exception as e:
                    print(f'server killed {e}')
                    self.socket.close()
                    sys.exit()

#__main__ : main 함수에서는 커맨드 라인 매개변수를 처리하고 다른 함수들을 호출
if __name__ == '__main__':
    parser = argparse.ArgumentParser(  # argparse : 커맨드 라인 인터페이스를 생성할 수 있게 해준다.(표준 라이브러리)
                                       # -> 매개변수를 지정하게 되면 파일 업로드나 명령어 실행 또는 셸 커맨드 개방 등의 용도로 사용할 수 있다.
        description='BHP Net Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        #--help를 지정했을 때 출력할 사용법 예시
        epilog=textwrap.dedent('''Example:
            netcat.py -t 192.168.1.108 -p 5555 -l -c # 셸 커맨드
            netcat.py -t 192.168.1.108 -p 5555 -l -u=mytest.whatisup # 파일 업로드
            netcat.py -t 192.168.1.108 -p 5555 -l -e=\"cat /etc/passwd\" # 명령어 실행
            echo 'ABCDEFGHI' | ./netcat.py -t 192.168.1.108 -p 135
            # 로컬에서 입력한 텍스트를 서버의 135번 포트로 전달
            netcat.py -t 192.168.1.108 -p 5555 #서버 연결
        '''))
    parser.add_argument('-c', '--command', action='store_true', help='initialize command shell') # -c : 대화형 셸 구성
    parser.add_argument('-e', '--execute', help='execute specified command') # -e : 특정 명령어 하나를 실행하기 원할 때 사용
    parser.add_argument('-l', '--listen', action='store_true', help='listen') # -l : 수신 측에서 반드시 설정
    parser.add_argument('-p', '--port', type=int, default=5555, help='specified port') # -p : 통신에 필요한 포트 번호 명시
    parser.add_argument('-t', '--target', default='192.168.1.203', help='specified IP') # -t : 공격 대상의 IP 주소를 지정
    parser.add_argument('-u', '--upload', help='upload file') # -u : 업로드하고자 하는 파일의 이름을 선택 가능
    args = parser.parse_args()
    # 이 프로그램은 수신 측과 송신 측에서 모두 사용 가능
    # 매개 변수를 통해 자신이 송신할 것인지, 수신받을 것인지를 선택
    # -c, -e 및 -u 옵션은 사실상 -l 옵션을 전제로 한다.
    # 송신 측에서는 수신 측과 연결을 수립해야 하므로 오직 -t와 -p 옵션을 통해 대상 호스트를 명시
    if args.listen: # 수신측에서 프로그램을 구동한다고 했을 때, 빈 문자열 버퍼를 생성한 후 NetCat 객체를 생성
        buffer = ''
    else: # 만약 송신측에서 구동한 경우라면 사용자의 입력을 stdin으로 받은 후 버퍼에 내용을 저장한다.
        buffer = sys.stdin.read()
    nc = NetCat(args, buffer.encode('utf-8'))
    nc.run() # NetCat 기능 구동을 위해 run() 함수를 호출
