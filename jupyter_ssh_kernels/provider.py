from jupyter_kernel_mgmt.discovery import KernelProviderBase
from jupyter_core.paths import jupyter_config_path
from pathlib import Path
import pytoml

from .launcher import launch, remote_launch_py

class SSHKernelProvider(KernelProviderBase):
    id = "simple-ssh"

    def find_kernels(self):
        names_seen = set()
        for cfg_dir in jupyter_config_path():
            cfg_file = Path(cfg_dir, 'ssh_kernels.toml')
            if not cfg_file.is_file():
                continue

            with cfg_file.open('r', encoding='utf-8') as f:
                config = pytoml.load(f)

            for name, kinfo in config['kernels'].items():
                # Files earlier in the search path shadow kernels from later ones
                if name in names_seen:
                    continue
                names_seen.add(name)

                yield (name, kinfo)

    def launch(self, name, cwd=None):
        for candidate_name, kinfo in self.find_kernels():
            if candidate_name == name:
                conn_info = launch(kinfo['address'], remote_launch_py(kinfo))
                return (conn_info, None)

        raise KeyError(name)
