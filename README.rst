This is experimental, to work with a branch not yet merged in jupyter_client.

Ensure that you can SSH to the target machine with no password.
Create a file ``~/.jupyter/ssh_kernels.toml`` with contents like this:

.. code-block:: ini

    [kernels.mydesktop]
    address = "10.15.41.11"
    argv = ["python3", "-m", "ipykernel_launcher", "-f", "{connection_file}"]
    cwd = "/home/takluyver/scratch"
    language = "python"

Then test with ``python3 -m jupyter_ssh_kernels``. It should start a kernel
over SSH, connect to it, get kernel info, and shut it down cleanly.
