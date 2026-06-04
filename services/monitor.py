import logging
from pathlib import Path

from psutil._ntuples import sdiskusage

from tools.disk_mount import find_mount_point_by_label
import utils.helpers as format_string
from psutil import (
    cpu_percent, cpu_stats, cpu_freq,  # cpu_info
    virtual_memory, swap_memory,  # memory_info (RAM)
    disk_partitions, disk_usage, disk_io_counters,  # Disks_info
    sensors_temperatures, sensors_fans, sensors_battery,  # Sensors_info
    net_connections, net_if_stats,  # Network_info
    users, boot_time,# Users_info
    AccessDenied, # Exception
)

logger = logging.getLogger(__name__)
DATA_UNAVAILABLE = "N/A"

def _safe_call_to_psutil(func, label: str, *args, **kwargs):
    """Call a psutil function and return its result, or DATA_UNAVAILABLE on AccessDenied.

    *args and **kwargs are forwarded to func because several psutil functions accept
    optional parameters (e.g cpu_percent(interval=), disk_io_counters(perdisk=),
    net_io_counters(pernic=)), so this wrapper stays general rather than hard-coding
    a fixed signature.
    """
    try:
        logger.info("Successfully collected %s" , label)
        return func(*args, **kwargs)

    except AccessDenied:
        logger.error("Access denied getting %s", label)
        return DATA_UNAVAILABLE

def _get_disk_space_usage(path: str) -> sdiskusage | str:
    """Return disk usage stats for path, or DATA_UNAVAILABLE if the path is absent or unreadable.

    Guards against empty strings, None, and non-existent paths before calling
    psutil.disk_usage so callers never need to handle OSError for missing mount points.
    """
    if not path:
        return DATA_UNAVAILABLE
    if path is None:
        return DATA_UNAVAILABLE
    if not Path(path).exists():
        logger.warning("Path does not exist: %s", path)
        return DATA_UNAVAILABLE
    try:
        return disk_usage(path)
    except AccessDenied:
        logger.error("Access denied: disk_usage(path=%s)", path)
        return DATA_UNAVAILABLE

# cpu_info

def collect_cpu_report() -> str:
    cpu_usage_percentage = _safe_call_to_psutil(cpu_percent, "cpu_percent")
    cpu_clock_frequency = _safe_call_to_psutil(cpu_freq, "cpu_freq")
    cpu_performance_counters = _safe_call_to_psutil(cpu_stats, "cpu_stats")
    return format_string.format_cpu(cpu_usage_percentage, cpu_clock_frequency, cpu_performance_counters)


#memory_info

def collect_memory_report() -> str:
    physical_memory_stats = _safe_call_to_psutil(virtual_memory, "virtual_memory")
    swap_space_stats = _safe_call_to_psutil(swap_memory, "swap_memory")
    return format_string.format_memory(physical_memory_stats, swap_space_stats)


# disks_info

def collect_disk_report()-> str:
    disk_mount_points = _safe_call_to_psutil(disk_partitions, "disk_partitions")
    disk_read_write_counters = _safe_call_to_psutil(disk_io_counters, "disk_io_counters")

    disk_space_at_path = _get_disk_space_usage("/")
    label_mount_point = find_mount_point_by_label()
    disk_space_at_path_2 = _get_disk_space_usage(label_mount_point)

    return format_string.format_disks(disk_mount_points, disk_space_at_path, disk_space_at_path_2, disk_read_write_counters)

# sensors_info

def collect_sensors_report() -> str:
    component_temperatures = _safe_call_to_psutil(sensors_temperatures, "sensors_temperatures")
    cooling_fan_speeds = _safe_call_to_psutil(sensors_fans, "sensors_fans")
    battery_charge_info = _safe_call_to_psutil(sensors_battery, "sensors_battery")
    return format_string.format_sensors(component_temperatures, cooling_fan_speeds, battery_charge_info)

# network_info

def collect_network_report() -> str:
    active_socket_connections = _safe_call_to_psutil(net_connections, "net_connections")
    network_interface_statistics = _safe_call_to_psutil(net_if_stats, "net_if_stats")
    return format_string.format_network(active_socket_connections, network_interface_statistics)

# users_info.py

def collect_users_report() -> str:
    current_logged_in_users = _safe_call_to_psutil(users, "users")
    last_system_boot_time = _safe_call_to_psutil(boot_time, "boot_time")
    return format_string.format_users(current_logged_in_users, last_system_boot_time)


def collect_general_report() -> str:
    users_info = _safe_call_to_psutil(users, "users")
    boot_time_info = _safe_call_to_psutil(boot_time, "boot_time")
    virtual_memory_stats = _safe_call_to_psutil(virtual_memory, "virtual_memory")
    sensors_temperature_info = _safe_call_to_psutil(sensors_temperatures, "sensors_temperatures")
    sensors_fan_info = _safe_call_to_psutil(sensors_fans, "sensors_fans")
    sensors_battery_info = _safe_call_to_psutil(sensors_battery, "sensors_battery")
    return format_string.format_general(
        users_info, boot_time_info, virtual_memory_stats,
        sensors_temperature_info, sensors_fan_info, sensors_battery_info,
    )
