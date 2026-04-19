# Formateo de mensajes y tablas
import time
from datetime import timedelta


# ── Privadas ──────────────────────────────────────────────────────────────────

def _bytes_to_human(n: int) -> str:
    _UNITS = ("B", "KB", "MB", "GB", "TB")
    value = float(n)
    for unit in _UNITS[:-1]:
        if value < 1024.0:
            return f"{value:.1f} {unit}"
        value /= 1024.0
    return f"{value:.1f} TB"


def _percent_emoji(percent: float) -> str:
    if percent < 60:
        return "🟢"
    elif percent <= 85:
        return "🟡"
    return "🔴"


# ── Existentes ────────────────────────────────────────────────────────────────

def format_cpu_status(percent, freq_current, freq_max):
    # Lógica de color para carga
    if percent < 60:
        emoji = "🟢"
    elif percent <= 85:
        emoji = "🟡"
    else:
        emoji = "🔴"

    # Formateo de frecuencia a GHz
    curr_ghz = freq_current / 1000 if freq_current > 1000 else freq_current
    max_ghz = freq_max / 1000 if freq_max > 1000 else freq_max

    return f"{int(percent)}% {emoji}\nFrecuencia: {curr_ghz:.1f} GHz (Máx: {max_ghz:.1f} GHz)"


def get_formatted_uptime(boot_timestamp):
    # Calcula la diferencia entre ahora y el arranque
    uptime_seconds = time.time() - boot_timestamp
    uptime_delta = timedelta(seconds=uptime_seconds)

    # Formatea a Horas:Minutos (descarta microsegundos)
    hours, remainder = divmod(int(uptime_delta.total_seconds()), 3600)
    minutes, _ = divmod(remainder, 60)

    return f"{hours}h {minutes}m"


# ── Formateadores por grupo ───────────────────────────────────────────────────

def format_cpu(percent, freq, stats) -> str:
    lines = ["CPU"]

    if percent == "N/A":
        lines.append("Usage: N/A")
    else:
        lines.append(f"Usage: {int(percent)}% {_percent_emoji(percent)}")

    if freq == "N/A":
        lines.append("Frequency: N/A")
    else:
        curr_ghz = freq.current / 1000 if freq.current > 1000 else freq.current
        max_ghz = freq.max / 1000 if freq.max > 1000 else freq.max
        lines.append(f"Frequency: {curr_ghz:.1f} GHz (Max: {max_ghz:.1f} GHz)")

    if stats == "N/A":
        lines.append("Stats: N/A")
    else:
        lines.append(f"Context switches: {stats.ctx_switches}")
        lines.append(f"Interrupts: {stats.interrupts}")
        lines.append(f"Soft interrupts: {stats.soft_interrupts}")
        lines.append(f"Syscalls: {stats.syscalls}")

    return "\n".join(lines)


def format_memory(virtual, swap) -> str:
    lines = ["Memory"]

    lines.append("RAM")
    if virtual == "N/A":
        lines.append("  N/A")
    else:
        lines.append(f"  Total: {_bytes_to_human(virtual.total)}")
        lines.append(f"  Used: {_bytes_to_human(virtual.used)} — {int(virtual.percent)}% {_percent_emoji(virtual.percent)}")
        lines.append(f"  Free: {_bytes_to_human(virtual.free)}")
        lines.append(f"  Available: {_bytes_to_human(virtual.available)}")
        lines.append(f"  Cache: {_bytes_to_human(virtual.cached)}")
        lines.append(f"  Buffers: {_bytes_to_human(virtual.buffers)}")

    lines.append("Swap")
    if swap == "N/A":
        lines.append("  N/A")
    else:
        lines.append(f"  Total: {_bytes_to_human(swap.total)}")
        lines.append(f"  Used: {_bytes_to_human(swap.used)} — {int(swap.percent)}% {_percent_emoji(swap.percent)}")
        lines.append(f"  Free: {_bytes_to_human(swap.free)}")

    return "\n".join(lines)


def format_disks(partitions, usage, io_counters) -> str:
    lines = ["Disks"]

    lines.append("Partitions")
    if partitions == "N/A":
        lines.append("  N/A")
    elif not partitions:
        lines.append("  No partitions found")
    else:
        for p in partitions:
            lines.append(f"  {p.device} → {p.mountpoint} ({p.fstype})")

    lines.append("Usage (/)")
    if usage == "N/A":
        lines.append("  N/A")
    else:
        lines.append(f"  Total: {_bytes_to_human(usage.total)}")
        lines.append(f"  Used: {_bytes_to_human(usage.used)} — {int(usage.percent)}% {_percent_emoji(usage.percent)}")
        lines.append(f"  Free: {_bytes_to_human(usage.free)}")

    lines.append("I/O")
    if io_counters is None or io_counters == "N/A":
        lines.append("  N/A")
    else:
        lines.append(f"  Reads: {io_counters.read_count} | Data read: {_bytes_to_human(io_counters.read_bytes)}")
        lines.append(f"  Writes: {io_counters.write_count} | Data written: {_bytes_to_human(io_counters.write_bytes)}")

    return "\n".join(lines)


def format_sensors(temperatures, fans, battery) -> str:
    lines = ["Sensors"]

    lines.append("Temperatures")
    if temperatures == "N/A":
        lines.append("  N/A")
    elif not temperatures:
        lines.append("  No temperature data")
    else:
        for name, readings in temperatures.items():
            for r in readings:
                label = r.label if r.label else name
                crit = f" (critical: {r.critical}°C)" if r.critical else ""
                lines.append(f"  {name} — {label}: {r.current:.1f}°C{crit}")

    lines.append("Fans")
    if fans == "N/A":
        lines.append("  N/A")
    elif not fans:
        lines.append("  No fans detected")
    else:
        for name, readings in fans.items():
            for r in readings:
                label = r.label if r.label else name
                lines.append(f"  {name} — {label}: {r.current} RPM")

    lines.append("Battery")
    if battery is None:
        lines.append("  No battery")
    elif battery == "N/A":
        lines.append("  N/A")
    else:
        if battery.secsleft == -1:
            time_left = "Calculating..."
        else:
            h, rem = divmod(int(battery.secsleft), 3600)
            m, _ = divmod(rem, 60)
            time_left = f"{h}h {m}m"
        lines.append(f"  Level: {int(battery.percent)}% {_percent_emoji(battery.percent)}")
        lines.append(f"  Status: {'Plugged in' if battery.power_plugged else 'On battery'}")
        lines.append(f"  Time remaining: {time_left}")

    return "\n".join(lines)


def format_network(connections, if_stats) -> str:
    lines = ["Network"]

    if connections == "N/A":
        lines.append("Connections: N/A")
    else:
        lines.append(f"Connections: {len(connections)}")
        status_counts = {}
        for c in connections:
            status_counts[c.status] = status_counts.get(c.status, 0) + 1
        for status, count in sorted(status_counts.items()):
            lines.append(f"  {status}: {count}")

    lines.append("Interfaces")
    if if_stats == "N/A":
        lines.append("  N/A")
    elif not if_stats:
        lines.append("  No interfaces detected")
    else:
        for name, nic in if_stats.items():
            state = "up" if nic.isup else "down"
            lines.append(f"  {name}: {state}, {nic.speed} Mbps")

    return "\n".join(lines)


def format_users(users, boot_time) -> str:
    lines = ["Users"]

    if users == "N/A":
        lines.append("  N/A")
    elif not users:
        lines.append("  No active users")
    else:
        for u in users:
            host = f" ({u.host})" if u.host else " (local)"
            lines.append(f"  {u.name} — {u.terminal}{host}")

    if boot_time == "N/A":
        lines.append("Uptime: N/A")
    else:
        lines.append(f"Uptime: {get_formatted_uptime(boot_time)}")

    return "\n".join(lines)
