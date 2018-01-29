"""Sent to Python on the remote system to launch a kernel."""

from jupyter_client.manager2 import KernelManager2
km = KernelManager2(kernel_cmd={argv!r}, cwd={cwd!r}, ip={address!r})
print("!!!Started, connection_file:", km.connection_file, '!!!', flush=True)
km.wait(None)
