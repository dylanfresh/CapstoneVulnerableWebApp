## This function allows the webpage to be launched on two servers at once

import subprocess
import sys


# Make sure we're running in the current Python interpreter
python_exe = sys.executable

# Ports for the two servers
ports = [5000, 5001]

processes = []

for port in ports:
    print(f"Starting Flask server on port {port}")
    # Launch each server in a new process
    p = subprocess.Popen([python_exe, "main.py", "--port", str(port)])
    processes.append(p)

# Wait for both servers
try:
    for p in processes:
        p.wait()
except KeyboardInterrupt:
    print("Shutting down servers...")
    for p in processes:
        p.terminate()
