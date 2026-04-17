from psutil import (
    cpu_percent, cpu_count, cpu_stats, cpu_freq, #cpu_info
    virtual_memory, swap_memory, #memory_info (RAM)
    disk_partitions, disk_usage, disk_io_counters, #Disks_info
    sensors_temperatures, sensors_fans, sensors_battery, #Sensors_info
    net_connections, net_if_stats, #Network_info
    users, boot_time, #Users_info
)


def get_cpu_percent():# Return a float representing the current system-wide CPU utilization as a percentage.
    return cpu_percent()

def get_cpu_count():# Return the number of logical CPUs in the system (similar to os.cpu_count) or None
    return cpu_count()

def get_cpu_stats():# Return various CPU statistics as a named tuple
    return cpu_stats()

def get_cpu_freq():# Return CPU frequency 
    return cpu_freq()


def get_virtual_memory():# Return statistics about system memory usage 
    return virtual_memory()

def get_swap_memory():# Return system swap memory statistics
    return swap_memory()


# disks_info.py
def get_disk_partitions():
# Return all mounted disk partitions as a list of named tuples including device, mount point and filesystem type,
# similarly to “df” command on UNIX. If all parameter is False it tries to distinguish and return physical devices only
    return disk_partitions()

def get_disk_usage(path="/"):# Return system-wide disk I/O statistics 
    return disk_usage(path)

def get_disk_io_counters():# Return system-wide disk I/O statistics 
    return disk_io_counters()

# sensors_info
def get_sensors_temperatures():# Return hardware temperatures.
    return sensors_temperatures()

def get_sensors_fans():# Return hardware fans speed
    return sensors_fans()

def get_sensors_battery():# Return hardware fans speed. 
    return sensors_battery() # power_plugged: True if the AC power cable is connected, False if not or None


# network_info
def get_net_connections():# Return system-wide socket connections as a list of named tuples
    return net_connections()

def get_net_if_stats():# Return information about each NIC (network interface card) installed on the system
    return net_if_stats()


# users_info.py
def get_users():# Return users currently connected
    return users()

def get_boot_time():# Return the system boot time expressed in seconds since the epoch (seconds since January 1, 1970, at midnight UTC)
    return boot_time()
