from psutil import (virtual_memory,
                    swap_memory)
import logging

def get_virtual_memory_info():
    vm = virtual_memory()
    return (f"Total: {vm.total}\n"
            f"Percent: {vm.percent}\n"
            f"Used: {vm.used}\n"
            f"Free: {vm.free}\n"
            f"Available: {vm.available}\n"
            f"Active: {vm.active}\n"
            f"Inactive: {vm.inactive}\n"
            f"Buffers: {vm.buffers}\n"
            f"Cached: {vm.cached}\n"
            f"Shared: {vm.shared}\n")

def get_swap_memory_info():
    sw = swap_memory()
    return (f"Total: {sw.total}\n"
            f"Percent: {sw.percent}\n"
            f"Used:{sw.used}\n"
            f"Free: {sw.free}\n"
            f"Sin: {sw.sin}\n"
            f"Sout: {sw.sout}")


