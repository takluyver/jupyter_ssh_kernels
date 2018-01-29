"""Sent to Python on the remote system to launch a kernel."""

from jupyter_client.manager2 import KernelManager2
km = KernelManager2(kernel_cmd={argv}, cwd={cwd}, ip={address})
print("!!!Started, connection_file:", km.connection_file, '!!!')
km.wait()
