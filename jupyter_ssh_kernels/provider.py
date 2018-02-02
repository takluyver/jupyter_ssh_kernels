from jupyter_client.discovery import KernelProviderBase
from .manager import SSHKernelManager, remote_launch_py

KERNELS = {
    'mydesktop': {
        'address': '10.15.41.11',
        'argv': ['python3', '-m', 'ipykernel_launcher', '-f', '{connection_file}'],
        'cwd': '/home/takluyver/scratch',
        'language': 'python',
    }
}

class SSHKernelProvider(KernelProviderBase):
    id = "simple-ssh"

    def find_kernels(self):
        return KERNELS.items()

    def launch(self, name, cwd=None):
        kinfo = KERNELS[name]
        return SSHKernelManager(kinfo['address'],
                                remote_launch_py(kinfo))
