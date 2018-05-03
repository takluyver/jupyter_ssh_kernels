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
print(kc.kernel_info().content)
print()

print("Executing some code...")
kc.execute_interactive("""
import time

for a in range(6):
    print(a)
    time.sleep(1)

input("Press enter to finish> ")
print("End of submitted code")
""")
print("Finished executing")

import time
time.sleep(2)
print("\nShutting down...")
kc.shutdown_or_terminate()
kc.close()
print("Shutdown complete")
