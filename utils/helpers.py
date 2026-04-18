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
        lines.append("Uso: N/A")
    else:
        lines.append(f"Uso: {int(percent)}% {_percent_emoji(percent)}")

    if freq == "N/A":
        lines.append("Frecuencia: N/A")
    else:
        curr_ghz = freq.current / 1000 if freq.current > 1000 else freq.current
        max_ghz = freq.max / 1000 if freq.max > 1000 else freq.max
        lines.append(f"Frecuencia: {curr_ghz:.1f} GHz (Máx: {max_ghz:.1f} GHz)")

    if stats == "N/A":
        lines.append("Estadísticas: N/A")
    else:
        lines.append(f"Cambios de contexto: {stats.ctx_switches}")
        lines.append(f"Interrupciones: {stats.interrupts}")
        lines.append(f"Interrupciones soft: {stats.soft_interrupts}")
        lines.append(f"Llamadas al sistema: {stats.syscalls}")

    return "\n".join(lines)


def format_memory(virtual, swap) -> str:
    lines = ["Memoria"]

    lines.append("RAM")
    if virtual == "N/A":
        lines.append("  N/A")
    else:
        lines.append(f"  Total: {_bytes_to_human(virtual.total)}")
        lines.append(f"  Usada: {_bytes_to_human(virtual.used)} — {int(virtual.percent)}% {_percent_emoji(virtual.percent)}")
        lines.append(f"  Libre: {_bytes_to_human(virtual.free)}")
        lines.append(f"  Disponible: {_bytes_to_human(virtual.available)}")
        lines.append(f"  Caché: {_bytes_to_human(virtual.cached)}")
        lines.append(f"  Búferes: {_bytes_to_human(virtual.buffers)}")

    lines.append("Swap")
    if swap == "N/A":
        lines.append("  N/A")
    else:
        lines.append(f"  Total: {_bytes_to_human(swap.total)}")
        lines.append(f"  Usada: {_bytes_to_human(swap.used)} — {int(swap.percent)}% {_percent_emoji(swap.percent)}")
        lines.append(f"  Libre: {_bytes_to_human(swap.free)}")

    return "\n".join(lines)


def format_disks(partitions, usage, io_counters) -> str:
    lines = ["Discos"]

    lines.append("Particiones")
    if partitions == "N/A":
        lines.append("  N/A")
    elif not partitions:
        lines.append("  Sin particiones detectadas")
    else:
        for p in partitions:
            lines.append(f"  {p.device} → {p.mountpoint} ({p.fstype})")

    lines.append("Uso (/)")
    if usage == "N/A":
        lines.append("  N/A")
    else:
        lines.append(f"  Total: {_bytes_to_human(usage.total)}")
        lines.append(f"  Usada: {_bytes_to_human(usage.used)} — {int(usage.percent)}% {_percent_emoji(usage.percent)}")
        lines.append(f"  Libre: {_bytes_to_human(usage.free)}")

    lines.append("E/S")
    if io_counters is None or io_counters == "N/A":
        lines.append("  N/A")
    else:
        lines.append(f"  Lecturas: {io_counters.read_count} | Datos leídos: {_bytes_to_human(io_counters.read_bytes)}")
        lines.append(f"  Escrituras: {io_counters.write_count} | Datos escritos: {_bytes_to_human(io_counters.write_bytes)}")

    return "\n".join(lines)


def format_sensors(temperatures, fans, battery) -> str:
    lines = ["Sensores"]

    lines.append("Temperaturas")
    if temperatures == "N/A":
        lines.append("  N/A")
    elif not temperatures:
        lines.append("  Sin datos de temperatura")
    else:
        for name, readings in temperatures.items():
            for r in readings:
                label = r.label if r.label else name
                crit = f" (crítico: {r.critical}°C)" if r.critical else ""
                lines.append(f"  {name} — {label}: {r.current:.1f}°C{crit}")

    lines.append("Ventiladores")
    if fans == "N/A":
        lines.append("  N/A")
    elif not fans:
        lines.append("  Sin ventiladores detectados")
    else:
        for name, readings in fans.items():
            for r in readings:
                label = r.label if r.label else name
                lines.append(f"  {name} — {label}: {r.current} RPM")

    lines.append("Batería")
    if battery is None:
        lines.append("  Sin batería")
    elif battery == "N/A":
        lines.append("  N/A")
    else:
        if battery.secsleft == -1:
            tiempo = "Calculando..."
        else:
            h, rem = divmod(int(battery.secsleft), 3600)
            m, _ = divmod(rem, 60)
            tiempo = f"{h}h {m}m"
        lines.append(f"  Nivel: {int(battery.percent)}% {_percent_emoji(battery.percent)}")
        lines.append(f"  Estado: {'Conectado' if battery.power_plugged else 'Batería'}")
        lines.append(f"  Tiempo restante: {tiempo}")

    return "\n".join(lines)


def format_network(io_counters, connections, if_stats) -> str:
    lines = ["Red"]

    lines.append("E/S")
    if io_counters is None or io_counters == "N/A":
        lines.append("  N/A")
    else:
        lines.append(f"  Enviado: {_bytes_to_human(io_counters.bytes_sent)} | Recibido: {_bytes_to_human(io_counters.bytes_recv)}")
        lines.append(f"  Paquetes enviados: {io_counters.packets_sent} | Paquetes recibidos: {io_counters.packets_recv}")
        lines.append(f"  Errores: {io_counters.errin} entrada / {io_counters.errout} salida")

    if connections == "N/A":
        lines.append("Conexiones: N/A")
    else:
        lines.append(f"Conexiones: {len(connections)}")
        status_counts = {}
        for c in connections:
            status_counts[c.status] = status_counts.get(c.status, 0) + 1
        for status, count in sorted(status_counts.items()):
            lines.append(f"  {status}: {count}")

    lines.append("Interfaces")
    if if_stats == "N/A":
        lines.append("  N/A")
    elif not if_stats:
        lines.append("  Sin interfaces detectadas")
    else:
        for name, nic in if_stats.items():
            estado = "activa" if nic.isup else "inactiva"
            lines.append(f"  {name}: {estado}, {nic.speed} Mbps")

    return "\n".join(lines)


def format_users(users, boot_time) -> str:
    lines = ["Usuarios"]

    if users == "N/A":
        lines.append("  N/A")
    elif not users:
        lines.append("  Sin usuarios conectados")
    else:
        for u in users:
            host = f" ({u.host})" if u.host else " (local)"
            lines.append(f"  {u.name} — {u.terminal}{host}")

    if boot_time == "N/A":
        lines.append("Tiempo activo: N/A")
    else:
        lines.append(f"Tiempo activo: {get_formatted_uptime(boot_time)}")

    return "\n".join(lines)
