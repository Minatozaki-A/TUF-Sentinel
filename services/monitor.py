from psutil import (
    cpu_percent, cpu_stats, cpu_freq,  # cpu_info
    virtual_memory, swap_memory,  # memory_info (RAM)
    disk_partitions, disk_usage, disk_io_counters,  # Disks_info
    sensors_temperatures, sensors_fans, sensors_battery,  # Sensors_info
    net_connections, net_if_stats,  # Network_info
    users, boot_time, AccessDenied,  # Users_info
)
import logging

logger = logging.getLogger(__name__)

def get_cpu_percent():# Return a float representing the current system-wide CPU utilization as a percentage.
    try:
        return cpu_percent()
    except AccessDenied:
        logger.error("Acceso denegado al obtener cpu_percent")
        return "N/A"

def get_cpu_stats():# Return various CPU statistics as a named tuple
    try:
        return cpu_stats()
    except AccessDenied:
        logger.error("Acceso denegado al obtener cpu_stats")
        return "N/A"

def get_cpu_freq():# Return CPU frequency
    try:
        return cpu_freq()
    except AccessDenied:
        logger.error("Acceso denegado al obtener cpu_freq")
        return "N/A"

#memory_info
def get_virtual_memory():# Return statistics about system memory usage
    try:
        return virtual_memory()
    except AccessDenied:
        logger.error("Acceso denegado al obtener virtual_memory")
        return "N/A"


def get_swap_memory():# Return system swap memory statistics
    try:
        return swap_memory()
    except AccessDenied:
        logger.error("Acceso denegado al obtener swap_memory")
        return "N/A"

# disks_info.py
def get_disk_partitions():
# Return all mounted disk partitions as a list of named tuples including device, mount point and filesystem type,
# similarly to "df" command on UNIX. If all parameter is False it tries to distinguish and return physical devices only
    try:
        return disk_partitions()
    except AccessDenied:
        logger.error("Acceso denegado al obtener disk_partitions")
        return "N/A"

def get_disk_usage(path="/"):# Return system-wide disk I/O statistics
    try:
        return disk_usage(path)
    except AccessDenied:
        logger.error("Acceso denegado al obtener disk_usage(path=%s)", path)
        return "N/A"

def get_disk_io_counters():# Return system-wide disk I/O statistics
    try:
        return disk_io_counters()
    except AccessDenied:
        logger.error("Acceso denegado al obtener disk_io_counters")
        return "N/A"

# sensors_info
def get_sensors_temperatures():# Return hardware temperatures.
    try:
        return sensors_temperatures()
    except AccessDenied:
        logger.error("Acceso denegado al obtener sensors_temperatures")
        return "N/A"

def get_sensors_fans():# Return hardware fans speed
    try:
        return sensors_fans()
    except AccessDenied:
        logger.error("Acceso denegado al obtener sensors_fans")
        return "N/A"


def get_sensors_battery():# Return hardware fans speed.
    try:
        return sensors_battery() # power_plugged: True if the AC power cable is connected, False if not or None
    except AccessDenied:
        logger.error("Acceso denegado al obtener sensors_battery")
        return "N/A"

# network_info
def get_net_connections():# Return system-wide socket connections as a list of named tuples
    try:
        return net_connections()
    except AccessDenied:
        logger.error("Acceso denegado al obtener net_connections")
        return "N/A"

def get_net_if_stats():# Return information about each NIC (network interface card) installed on the system
    try:
        return net_if_stats()
    except AccessDenied:
        logger.error("Acceso denegado al obtener net_if_stats")
        return "N/A"

# users_info.py
def get_users():# Return users currently connected
    try:
        return users()
    except AccessDenied:
        logger.error("Acceso denegado al obtener users")
        return "N/A"

def get_boot_time():# Return the system boot time expressed in seconds since the epoch (seconds since January 1, 1970, at midnight UTC)
    try:
        return boot_time()
    except AccessDenied:
        logger.error("Acceso denegado al obtener boot_time")
        return "N/A"
