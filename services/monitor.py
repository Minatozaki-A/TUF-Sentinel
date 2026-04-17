from psutil import (
    cpu_times, cpu_percent, cpu_times_percent, cpu_count, cpu_stats, cpu_freq,
    virtual_memory, swap_memory,
    disk_partitions, disk_usage, disk_io_counters,
   # pids, Process,
    sensors_temperatures, sensors_fans, sensors_battery,
    net_io_counters, net_connections, net_if_addrs, net_if_stats,
    users, boot_time,
)


# cpu_info.py
def get_cpu_times():
    return cpu_times()

def get_cpu_percent():
    return cpu_percent()

def get_cpu_times_percent():
    return cpu_times_percent()

def get_cpu_count():
    return cpu_count()

def get_cpu_stats():
    return cpu_stats()

def get_cpu_freq():
    return cpu_freq()


# memory_info.py
def get_virtual_memory():
    return virtual_memory()

def get_swap_memory():
    return swap_memory()


# heap_infomation.py
# heap_info no es una función real de psutil — ImportError en el módulo original


# disks_info.py
def get_disk_partitions():
    return disk_partitions()

def get_disk_usage(path="/"):
    return disk_usage(path)

def get_disk_io_counters():
    return disk_io_counters()


# process_management.py
#def get_pids():
#    return pids()
#
#def get_process(pid):
#    return Process(pid)


# sensors_info.py
def get_sensors_temperatures():
    return sensors_temperatures()

def get_sensors_fans():
    return sensors_fans()

def get_sensors_battery():
    return sensors_battery()


# network_info.py
def get_net_io_counters():
    return net_io_counters()

def get_net_connections():
    return net_connections()

def get_net_if_addrs():
    return net_if_addrs()

def get_net_if_stats():
    return net_if_stats()


# users_info.py
def get_users():
    return users()

def get_boot_time():
    return boot_time()
