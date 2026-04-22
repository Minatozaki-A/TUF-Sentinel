import logging
from utils.helpers import *
from psutil import (
    cpu_percent, cpu_stats, cpu_freq,  # cpu_info
    virtual_memory, swap_memory,  # memory_info (RAM)
    disk_partitions, disk_usage, disk_io_counters,  # Disks_info
    sensors_temperatures, sensors_fans, sensors_battery,  # Sensors_info
    net_connections, net_if_stats,  # Network_info
    users, boot_time,# Users_info
    AccessDenied # Exception
)

logger = logging.getLogger(__name__)
DATA_UNAVAILABLE = "N/A"

def _safe_call_to_psutil(func, label: str):
    try:
        return func()
    except AccessDenied:
        logger.error("Access denied getting %s", label)
        return DATA_UNAVAILABLE


# cpu_info
def get_cpu_utilization():
    try:
        return cpu_percent()
    except AccessDenied:
        logger.error("Access denied getting cpu_percent")
        return DATA_UNAVAILABLE

def get_cpu_statistics():
    try:
        return cpu_stats()
    except AccessDenied:
        logger.error("Access denied getting cpu_stats")
        return DATA_UNAVAILABLE

def get_cpu_frequency():
    try:
        return cpu_freq()
    except AccessDenied:
        logger.error("Access denied getting cpu_freq")
        return DATA_UNAVAILABLE

def collect_cpu_report():
    cpu_usage_percentage = _safe_call_to_psutil(cpu_percent, "cpu_percent")
    cpu_clock_frequency = _safe_call_to_psutil(cpu_freq, "cpu_freq")
    cpu_performance_counters = _safe_call_to_psutil(cpu_stats, "cpu_stats")
    return format_cpu(cpu_usage_percentage, cpu_clock_frequency, cpu_performance_counters)


#memory_info
def get_ram_usage():
    try:
        return virtual_memory()
    except AccessDenied:
        logger.error("Access denied getting virtual_memory")
        return DATA_UNAVAILABLE

def collect_memory_report():
    physical_memory_stats = _safe_call_to_psutil(virtual_memory, "virtual_memory")
    swap_space_stats = _safe_call_to_psutil(swap_memory, "swap_memory")
    return format_memory(physical_memory_stats, swap_space_stats)


# disks_info.py
def get_mounted_partitions():
    try:
        return disk_partitions()
    except AccessDenied:
        logger.error("Access denied getting disk_partitions")
        return DATA_UNAVAILABLE

def get_disk_space_usage(path: str):
    try:
        return disk_usage(path)
    except AccessDenied:
        logger.error("Access denied getting disk_usage(path=%s)", path)
        return DATA_UNAVAILABLE

def collect_disk_report(path: str):
    disk_mount_points = _safe_call_to_psutil(disk_partitions, "disk_partitions")
    disk_space_at_path = get_disk_space_usage(path)
    disk_read_write_counters = _safe_call_to_psutil(disk_io_counters, "disk_io_counters")
    return format_disks(disk_mount_points, disk_space_at_path, disk_read_write_counters)

# sensors_info
def get_hardware_temperatures():
    try:
        return sensors_temperatures()
    except AccessDenied:
        logger.error("Access denied getting sensors_temperatures")
        return DATA_UNAVAILABLE

def collect_sensors_report():
    component_temperatures = _safe_call_to_psutil(sensors_temperatures, "sensors_temperatures")
    cooling_fan_speeds = _safe_call_to_psutil(sensors_fans, "sensors_fans")
    battery_charge_info = _safe_call_to_psutil(sensors_battery, "sensors_battery")
    return format_sensors(component_temperatures, cooling_fan_speeds, battery_charge_info)

# network_info
def get_network_connections():
    try:
        return net_connections()
    except AccessDenied:
        logger.error("Access denied getting net_connections")
        return DATA_UNAVAILABLE

def get_network_interface_stats():
    try:
        return net_if_stats()
    except AccessDenied:
        logger.error("Access denied getting net_if_stats")
        return DATA_UNAVAILABLE

def collect_network_report():
    active_socket_connections = _safe_call_to_psutil(net_connections, "net_connections")
    network_interface_statistics = _safe_call_to_psutil(net_if_stats, "net_if_stats")
    return format_network(active_socket_connections, network_interface_statistics)

# users_info.py
def get_logged_in_users():
    try:
        return users()
    except AccessDenied:
        logger.error("Access denied getting users")
        return DATA_UNAVAILABLE

def collect_users_report():
    current_logged_in_users = _safe_call_to_psutil(users, "users")
    last_system_boot_time = _safe_call_to_psutil(boot_time, "boot_time")
    return format_users(current_logged_in_users, last_system_boot_time)