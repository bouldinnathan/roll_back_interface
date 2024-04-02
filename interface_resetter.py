#!/usr/bin/env python3
import subprocess
import time

def is_ip_reachable(ip_address):
    """Check if the IP address is reachable."""
    try:
        # Ping the IP address
        subprocess.check_output(["ping", "-c", "1", ip_address], stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError:
        return False

def overwrite_file_from_source(target_file_path, source_file_path):
    """Overwrite the target file with data from the source file."""
    with open(source_file_path, "r") as source_file:
        data = source_file.read()
    with open(target_file_path, "w") as target_file:
        target_file.write(data)

def reload_network_interfaces():
    """Reload the network interfaces using the 'ifreload' command."""
    try:
        subprocess.check_output(["ifreload", "-a"])
        print("Network interfaces reloaded successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to reload network interfaces: {e}")

def monitor_ip_and_overwrite_file(ip_address, target_file_path, source_file_path, timeout=60):
    """Monitor the IP address and overwrite the target file with data from the source file if the IP becomes unreachable for the specified timeout."""
    unreachable_start = None

    while True:
        if is_ip_reachable(ip_address):
            print(f"{ip_address} is reachable.")
            unreachable_start = None  # Reset the timer
        else:
            print(f"{ip_address} is unreachable.")
            if unreachable_start is None:
                unreachable_start = time.time()
            elif time.time() - unreachable_start >= timeout:
                print(f"{ip_address} has been unreachable for {timeout} seconds. Overwriting the file and reloading network interfaces.")
                overwrite_file_from_source(target_file_path, source_file_path)
                reload_network_interfaces()
                break  # Exit the loop

        time.sleep(5)  # Check every 5 seconds
# Example usage
ip_address = "192.168.1.1"
target_file_path = '''/etc/network/interfaces'''
source_file_path = '''/etc/network/interfaces.old'''

if is_ip_reachable(ip_address):overwrite_file_from_source(source_file_path, target_file_path) # if router is connect then good config overwrite .old
# Will reset if the connection is lost
monitor_ip_and_overwrite_file(ip_address, target_file_path, source_file_path)
# cat /etc/network/interfaces > /etc/network/interfaces.old
