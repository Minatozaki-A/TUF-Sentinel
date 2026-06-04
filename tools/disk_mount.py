import logging
from pathlib import Path

from psutil import disk_partitions

from utils.config import collect_info_by_env

def find_mount_point_by_label()-> str | None:
    label_mount = collect_info_by_env("LABEL_MOUNT")
    parent_path = Path("/mnt")
    if not label_mount:
        raise ValueError("label_mount is empty")

    for part in disk_partitions():
        mount_point = Path(part.mountpoint)

        if mount_point.parent == parent_path and mount_point.name == label_mount:
            logging.info("SSD found - device: %s | mount point: %s | filesystem: %s",
                        part.device, part.mountpoint, part.fstype)
            return part.mountpoint
    return None

