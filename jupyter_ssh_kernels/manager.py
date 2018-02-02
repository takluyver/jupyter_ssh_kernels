import json
from jupyter_client.manager2 import KernelManager2ABC
from paramiko import SSHClient
from pathlib import Path
import re

def remote_launch_py(kinfo):
    rl_path = Path(__file__).parent / 'remote_launch.py'
    with rl_path.open() as f:
        return f.read().format(**kinfo)

CONN_FILE_RE = r"!!!Started, connection_file: (.*) !!!"

class SSHKernelManager(KernelManager2ABC):
    def __init__(self, server, remote_code):
        self.ssh_client = client = SSHClient()
        client.load_system_host_keys()
        client.connect(server)
        stdin, stdout, stderr = client.exec_command('python3')
        self.kernel_proc_channel = stdin.channel
        stdin.write(remote_code)
        stdin.close()
        self.kernel_proc_channel.shutdown_write()  # Sends EOF

        for line in stdout:
            m = re.match(CONN_FILE_RE, line)
            if m:
                remote_conn_file = m.group(1)
                break
        else:
            print('Exit status', self.kernel_proc_channel.exit_status)
            print("Stderr:")
            print(stderr.read().decode())
            print("Stdout:")
            print(stdout.read())
            raise RuntimeError("Remote kernel failed to start")

        print("Remote connection file:", remote_conn_file)
        with client.open_sftp() as sftp:
            with sftp.open(remote_conn_file) as f:
                self.connection_info = json.load(f)
    
    
    def is_alive(self):
        return not self.kernel_proc_channel.exit_status_ready()

    def wait(self, timeout):
        return not self.kernel_proc_channel.status_event.wait(timeout)
    
    def interrupt(self):
        pass
    
    def kill(self):
        pass
    
    def signal(self, signum):
        pass
    
    def cleanup(self):
        self.kernel_proc_channel.close()
        self.ssh_client.close()

    def get_connection_info(self):
        return self.connection_info

    def relaunch(self):
        pass
