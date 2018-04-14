"""Sent to Python on the remote system to launch a kernel."""

from jupyter_kernel_mgmt.subproc import SubprocessKernelLauncher
from jupyter_kernel_mgmt.nanny import KernelNanny
l = SubprocessKernelLauncher(kernel_cmd={argv!r}, cwd={cwd!r}, ip={address!r})
conn_info, mgr = l.launch()
nanny = KernelNanny(conn_info, mgr)
print("!!!Started, connection_file:", nanny.connection_file, '!!!', flush=True)
km.wait(None)
