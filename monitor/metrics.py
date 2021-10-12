
import psutil

from . import DU_PATH


def get_cpu_usage():
    """Get the current CPU usage."""
    return psutil.cpu_percent()


def get_disk_usage():
    """Get the current disk usage."""
    return psutil.disk_usage(DU_PATH).percent


def get_mem_usage():
    """Get the current memory usage."""
    return psutil.virtual_memory().percent


def get_total_packets_received_this_session():
    """Get the total number of packets received in this session."""
    return psutil.net_io_counters().packets_recv
