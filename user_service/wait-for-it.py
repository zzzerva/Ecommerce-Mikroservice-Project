#!/usr/bin/env python3
import socket
import time
import sys
import subprocess

def wait_for_port(host, port, timeout=30):
    start_time = time.time()
    while True:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except (socket.timeout, socket.error):
            if time.time() - start_time > timeout:
                return False
            time.sleep(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: wait-for-it.py host:port [-- command]")
        sys.exit(1)

    host, port = sys.argv[1].split(":")
    port = int(port)

    print(f"Waiting for {host}:{port}...")
    if not wait_for_port(host, port):
        print(f"Timeout waiting for {host}:{port}")
        sys.exit(1)

    print(f"{host}:{port} is available")

    if len(sys.argv) > 3 and sys.argv[2] == "--":
        command = sys.argv[3:]
        sys.exit(subprocess.call(command)) 