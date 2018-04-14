from jupyter_kernel_mgmt.client import BlockingKernelClient
from .provider import SSHKernelProvider

# Try starting a remote kernel and connecting to it.
conn_info, km = SSHKernelProvider().launch('mydesktop')
print("Started remote kernel")
print()
print(conn_info)
print()

kc = BlockingKernelClient(conn_info, km)
print("Getting kernel info...")
print(kc.kernel_info(reply=True).content)
print()

import time
time.sleep(5)
print("Shutting down...")
kc.shutdown_or_terminate()
print("Shutdown complete")
