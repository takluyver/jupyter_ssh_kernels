from jupyter_client.client2 import BlockingKernelClient2
from jupyter_client.manager2 import shutdown
from .jupyter_ssh_kernels import SSHKernelProvider

# Try starting a remote kernel and connecting to it.
km = SSHKernelProvider().launch('mydesktop')
print("Started remote kernel")
print()
print(km.get_connection_info())
print()

kc = BlockingKernelClient2(km.get_connection_info(), km)
print("Getting kernel info...")
print(kc.kernel_info(reply=True)['content'])
print()

import time
time.sleep(5)
print("Shutting down...")
shutdown(kc, km)
print("Shutdown complete")
