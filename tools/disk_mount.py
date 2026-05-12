import logging
from psutil import disk_partitions


def find_mount_point_by_label(label_mount: str = None)-> str | None:

    if not label_mount:
        raise ValueError("label_mount is empty")

    for part in disk_partitions():
        mount_point = part.mountpoint.rstrip('/')
        if mount_point.endswith(label_mount):
            logging.info("SSD found - device: %s | mount point: %s | filesystem: %s",
                        part.device, part.mountpoint, part.fstype)
            return part.mountpoint
    return None
