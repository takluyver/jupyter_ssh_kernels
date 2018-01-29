import json
from jupyter_client.client2 import BlockingKernelClient2
from jupyter_client.discovery import KernelProviderBase
from jupyter_client.manager2 import KernelManager2ABC, shutdown
from paramiko import SSHClient
import re

KERNELS = {
    'mydesktop': {
        'address': '10.15.41.11',
        'argv': ['python3', '-m', 'ipykernel_launcher', '-f', '{connection_file}'],
        'cwd': '/home/takluyver/scratch',
        'language': 'python',
    }
}

def remote_launch_py(kinfo):
    with open('remote_launch.py') as f:
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
        return True

    def wait(self, timeout):
        return not self.kernel_proc_channel.status_event.wait(timeout)
    
    def interrupt(self):
        pass
    
    def kill(self):
        pass
    
    def signal(self):
        pass
    
    def cleanup(self):
        self.kernel_proc_channel.close()
        self.ssh_client.close()

    def get_connection_info(self):
        return self.connection_info

    def relaunch(self):
        pass

class SSHKernelProvider(KernelProviderBase):
    id = "simple-ssh"
    
    def find_kernels(self):
        return KERNELS.items()

    def launch(self, name, cwd=None):
        kinfo = KERNELS[name]
        return SSHKernelManager(kinfo['address'],
                                remote_launch_py(kinfo))

if __name__ == '__main__':
    km = SSHKernelProvider().launch('mydesktop')
    print("Started remote kernel")
    print()
    print(km.get_connection_info())
    
    import time
    try:
        while True:
            time.sleep(1000)
    except KeyboardInterrupt:
        print("Attempting shutdown")
        kc = BlockingKernelClient2(km.get_connection_info(), km)
        shutdown(kc, km)
        print("Shutdown complete")
