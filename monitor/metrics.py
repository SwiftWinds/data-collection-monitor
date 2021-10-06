
import re
import subprocess

import psutil

# Pattern for matching the received packets in the output of `ifconfig`.
PACKETS_RECEIVED = re.compile(r'RX packets\s+(\d+)')


def get_cpu_usage():
    """Get the current CPU usage."""
    return psutil.cpu_percent()


def get_mem_usage():
    """Get the current memory usage."""
    return psutil.virtual_memory().percent


def get_total_packets_received_this_session():
    """Get the total number of packets received in this session."""
    total = 0
    lines = subprocess.run(
        ['ifconfig', '-a'],
        stdout=subprocess.PIPE
    ).stdout.decode('ascii').split('\n')
    for line in lines:
        m = re.search(PACKETS_RECEIVED, line)
        if m:
            total += int(m.group(1))
    return total
