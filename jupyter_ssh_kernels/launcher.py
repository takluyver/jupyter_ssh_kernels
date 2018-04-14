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

def launch(server, remote_code):
    client = SSHClient()
    client.load_system_host_keys()
    client.connect(server)
    stdin, stdout, stderr = client.exec_command('python3')
    stdin.write(remote_code)
    stdin.close()
    stdin.channel.shutdown_write()  # Sends EOF

    for line in stdout:
        m = re.match(CONN_FILE_RE, line)
        if m:
            remote_conn_file = m.group(1)
            break
    else:
        print('Exit status', stdin.channel.exit_status)
        print("Stderr:")
        print(stderr.read().decode())
        print("Stdout:")
        print(stdout.read())
        raise RuntimeError("Remote kernel failed to start")

    print("Remote connection file:", remote_conn_file)
    with client.open_sftp() as sftp:
        with sftp.open(remote_conn_file) as f:
            return json.load(f)
