from paramiko import SSHClient, SFTPClient, AutoAddPolicy
from socket import socket, AF_INET, SOCK_DGRAM
from pathlib import Path
import sys


class Busho:
    def __init__(self, project_path):
        self.project_path = project_path
        self.running_host = self._get_local_host()
        self.local_host_info = None
        self.remote_host_set = {}

    def local_host(self, host):
        def wrapper(func):
            assert not self.local_host_info
            self.local_host_info = {
                'host': host,
                'function': func,
            }
        return wrapper

    def remote_host(self, host, username, password, to_path='.'):
        def wrapper(func=None):
            self.remote_host_set[host] = {
                'host': host,
                'username': username,
                'password': password,
                'function': func,
                'to_path': to_path,
            }
        return wrapper

    def deploy(self):
        if self.local_host_info['host'] == self.running_host:
            for host_info in self.remote_host_set.values():
                self._init_project(host_info)
            self.local_host_info['function']()
        else:
            self.remote_host_set[self.running_host]['function']()

    @staticmethod
    def _get_local_host():
        with socket(AF_INET, SOCK_DGRAM) as s:
            s.connect(('8.8.8.8', 80))
            return s.getsockname()[0]

    def _init_project(self, host_info):
        with SSHClient() as ssh:
            ssh.set_missing_host_key_policy(AutoAddPolicy())
            ssh.connect(hostname=host_info['host'], username=host_info['username'], password=host_info['password'])
            with SFTPClient.from_transport(ssh.get_transport()) as sftp:
                self._upload_project(ssh, sftp, self.project_path, host_info['to_path'])
            try:
                execute_path = sys.argv[0].replace(self.project_path, self.project_path.split('/')[-1])
                *_, stderr = ssh.exec_command(f'python3 {execute_path}', timeout=5)
                stderr = stderr.read()
            except TimeoutError:
                stderr = False
            if stderr:
                print(host_info['host'], f'--- Error: {stderr.decode()}')
            else:
                print(host_info['host'], 'Success')

    def _upload_project(self, ssh, sftp, file_path, root_path):
        file_path = Path(file_path)
        root_path = f'{root_path}/{file_path.name}'
        if file_path.is_dir():
            ssh.exec_command(f'mkdir -p {root_path}')[1].read()
            for f in file_path.iterdir():
                self._upload_project(ssh, sftp, file_path / f.name, f'{root_path}')
        else:
            sftp.put(file_path, f'{root_path}')
