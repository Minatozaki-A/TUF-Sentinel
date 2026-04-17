# Formateo de mensajes y tablas
import time
from datetime import timedelta


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