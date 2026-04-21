from psutil import (
    cpu_percent, cpu_stats, cpu_freq,  # cpu_info
    virtual_memory, swap_memory,  # memory_info (RAM)
    disk_partitions, disk_usage, disk_io_counters,  # Disks_info
    sensors_temperatures, sensors_fans, sensors_battery,  # Sensors_info
    net_connections, net_if_stats,  # Network_info
    users, boot_time,# Users_info
    AccessDenied # Exception
)
import logging
from utils.helpers import *

logger = logging.getLogger(__name__)
# cpu_info
def get_cpu_percent():# Return a float representing the current system-wide CPU utilization as a percentage.
    try:
        return cpu_percent()
    except AccessDenied:
        logger.error("Access denied getting cpu_percent")
        return "N/A"

def get_cpu_stats():# Return various CPU statistics as a named tuple
    try:
        return cpu_stats()
    except AccessDenied:
        logger.error("Access denied getting cpu_stats")
        return "N/A"

def get_cpu_freq():# Return CPU frequency
    try:
        return cpu_freq()
    except AccessDenied:
        logger.error("Access denied getting cpu_freq")
        return "N/A"


def information_cpu():
    try:
        percent_info = cpu_percent()
        freq_info = cpu_freq()
        stats_info = cpu_stats()
    except AccessDenied:
        logger.error("Access denied getting cpu_percent, cpu_freq or cpu_stats")
        percent_info, freq_info, stats_info = "N/A", "N/A", "N/A"
    return format_cpu(percent_info, freq_info, stats_info)


#memory_info
def get_virtual_memory():# Return statistics about system memory usage
    try:
        return virtual_memory()
    except AccessDenied:
        logger.error("Access denied getting virtual_memory")
        return "N/A"


def get_swap_memory():# Return system swap memory statistics
    try:
        return swap_memory()
    except AccessDenied:
        logger.error("Access denied getting swap_memory")
        return "N/A"

def information_memory():
    try:
        vm_info = virtual_memory()
        swap_info = swap_memory()
    except AccessDenied:
        logger.error("Access denied getting virtual_memory or swap_memory")
        vm_info, swap_info = "N/A", "N/A"
    return format_memory(vm_info, swap_info)

# disks_info.py
def get_disk_partitions():
# Return all mounted disk partitions as a list of named tuples including device, mount point and filesystem type,
# similarly to "df" command on UNIX. If all parameter is False it tries to distinguish and return physical devices only
    try:
        return disk_partitions()
    except AccessDenied:
        logger.error("Access denied getting disk_partitions")
        return "N/A"

def get_disk_usage(path: str):# Return system-wide disk I/O statistics
    try:
        return disk_usage(path)
    except AccessDenied:
        logger.error("Access denied getting disk_usage(path=%s)", path)
        return "N/A"

def get_disk_io_counters():# Return system-wide disk I/O statistics
    try:
        return disk_io_counters()
    except AccessDenied:
        logger.error("Access denied getting disk_io_counters")
        return "N/A"


def information_disk(path: str):
    try:
        partitions_info = disk_partitions()
        usage_info = disk_usage(path)
        io_counters_info = disk_io_counters()
    except AccessDenied:
        logger.error("Access denied getting disk_partitions, disk_usage(path=%s)", path)
        partitions_info, usage_info, io_counters_info = "N/A", "N/A", "N/A"
    return format_disks(partitions_info, usage_info, io_counters_info)

# sensors_info
def get_sensors_temperatures():# Return hardware temperatures.
    try:
        return sensors_temperatures()
    except AccessDenied:
        logger.error("Access denied getting sensors_temperatures")
        return "N/A"

def get_sensors_fans():# Return hardware fans speed
    try:
        return sensors_fans()
    except AccessDenied:
        logger.error("Access denied getting sensors_fans")
        return "N/A"


def get_sensors_battery():# Return hardware fans speed.
    try:
        return sensors_battery() # power_plugged: True if the AC power cable is connected, False if not or None
    except AccessDenied:
        logger.error("Access denied getting sensors_battery")
        return "N/A"


def information_sensors():
    try:
        temperatures_info = sensors_temperatures()
        fans_info = sensors_fans()
        battery_info = sensors_battery()
    except AccessDenied:
        logger.error("Access denied getting sensors_temperatures, sensors_fans or sensors_battery")
        temperatures_info, fans_info, battery_info = "N/A", "N/A", "N/A"
    return format_sensors(temperatures_info, fans_info, battery_info)

# network_info
def get_net_connections():# Return system-wide socket connections as a list of named tuples
    try:
        return net_connections()
    except AccessDenied:
        logger.error("Access denied getting net_connections")
        return "N/A"

def get_net_if_stats():# Return information about each NIC (network interface card) installed on the system
    try:
        return net_if_stats()
    except AccessDenied:
        logger.error("Access denied getting net_if_stats")
        return "N/A"

def information_network():
    try:
        connections_info = net_connections()
        interfaces_info = net_if_stats()
    except AccessDenied:
        logger.error("Access denied getting net_connections or net_if_stats")
        connections_info, interfaces_info = "N/A", "N/A"
    return format_network(connections_info, interfaces_info)

# users_info.py
def get_users():# Return users currently connected
    try:
        return users()
    except AccessDenied:
        logger.error("Access denied getting users")
        return "N/A"

def get_boot_time():# Return the system boot time expressed in seconds since the epoch (seconds since January 1, 1970, at midnight UTC)
    try:
        return boot_time()
    except AccessDenied:
        logger.error("Access denied getting boot_time")
        return "N/A"

def information_users():
    try:
        users_info = users()
        boot_time_info = boot_time()
    except AccessDenied:
        logger.error("Access denied getting users or boot_time")
        users_info, boot_time_info = "N/A", "N/A"
    return format_users(users_info, boot_time_info)