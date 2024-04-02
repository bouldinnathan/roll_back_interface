# Network Configuration Monitor and Restorer

This Python script continuously monitors the reachability of a specified IP address (typically your router or gateway). If the IP address becomes unreachable for a specified duration, the script will revert the network configuration to a previously saved state and attempt to reload the network interfaces. This can be useful in situations where a poor network configuration change might otherwise leave you without remote access to the system.

## Prerequisites

- Python 3.x
- Linux operating system with `ifreload` command available (usually part of the `ifupdown2` package)

## Usage

1. **Initial Setup:**

   Before running the script for the first time, ensure that you have a known good network configuration file saved as `/etc/network/interfaces.old`. This file will be used to restore the network configuration if the specified IP becomes unreachable.

   You can create this file by copying your current configuration (or running the program with a good configuration):

   ```bash
   cp /etc/network/interfaces /etc/network/interfaces.old
   ```

2. **Configuration:**

   Open the script in a text editor and modify the following variables at the end of the script according to your network setup:

   - `ip_address`: Set this to the IP address you want to monitor (e.g., your router's IP).
   - `target_file_path`: Set this to the path of your active network configuration file (e.g., `/etc/network/interfaces`).
   - `source_file_path`: Set this to the path of your backup network configuration file (e.g., `/etc/network/interfaces.old`).

3. **Running the Script:**

   Run the script using Python 3. To ensure that the script continues to run in the background even if you log out, you can use `nohup`:

   ```bash
   nohup python3 network_monitor.py &
   ```

   Replace `network_monitor.py` with the name of your script file. The script will start monitoring the specified IP address and will overwrite the active network configuration with the backup configuration if the IP becomes unreachable for 60 seconds. It will then attempt to reload the network interfaces.

## Notes

- The script is configured to check the reachability of the IP address every 5 seconds. You can adjust this interval by modifying the `time.sleep(5)` line in the script.
- The script currently uses a timeout of 60 seconds to determine if the IP address is unreachable. You can adjust this duration by modifying the `timeout=60` parameter in the `monitor_ip_and_overwrite_file` function call.
- Ensure that the user running the script has the necessary permissions to modify the network configuration files and execute the `ifreload -a` command.

## License

This script is provided "as is", without warranty of any kind, express or implied. Use at your own risk.
