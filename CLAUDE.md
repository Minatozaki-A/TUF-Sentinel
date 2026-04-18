# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

**TUF-Sentinel** is a Telegram bot for system monitoring, written in Python. It exposes system metrics (CPU, memory, disk, network, processes, sensors, users) via Telegram commands using `psutil`.

Only `/hello` and `/memory` commands are fully implemented. The remaining psutil wrappers exist in `services/monitor.py` but have no corresponding Telegram handlers yet.

## Environment

This project uses [uv](https://docs.astral.sh/uv/) for dependency management and requires **Python >= 3.13**.

```bash
uv sync          # Install dependencies
uv run main.py   # Run the bot
uv add <package> # Add a dependency
```

There are no tests, no linting configuration, and no CI pipeline.

## Dependencies

Declared in `pyproject.toml`:
- `psutil >= 7.2.2` — system and process metrics
- `python-telegram-bot >= 22.7` — Telegram Bot API wrapper (async)

## Architecture

`main.py` registers async command handlers on a `telegram.ext.Application` and runs polling. It currently imports only from `services/monitor.py`.

`services/monitor.py` is the **canonical service module** — a consolidated psutil wrapper with functions grouped by category:
- **CPU** (6): `get_cpu_times`, `get_cpu_percent`, `get_cpu_times_percent`, `get_cpu_count`, `get_cpu_stats`, `get_cpu_freq`
- **Memory** (2): `get_virtual_memory`, `get_swap_memory`
- **Disks** (3): `get_disk_partitions`, `get_disk_usage(path="/")`, `get_disk_io_counters`
- **Processes** (2): `get_pids`, `get_process(pid)`
- **Sensors** (3): `get_sensors_temperatures`, `get_sensors_fans`, `get_sensors_battery`
- **Network** (4): `get_net_io_counters`, `get_net_connections`, `get_net_if_addrs`, `get_net_if_stats`
- **Users** (2): `get_users`, `get_boot_time`

The other files in `services/` (`cpu_info.py`, `disks_info.py`, `memory_info.py`, etc.) are legacy stubs containing only psutil imports. They are superseded by `monitor.py` and should not be imported.

## Implementing a New Command

1. Add an `async def <name>_handler(update, context)` in `main.py`.
2. Import the relevant function from `services/monitor.py` and reply with `await update.message.reply_text(result)`.
3. Register: `app.add_handler(CommandHandler("<command>", <name>_handler))`.

Service functions return psutil namedtuples directly — format the values in the handler, not in the service layer.

## Bot Token

The token is hardcoded as `"Token"` in `main.py:29`. Replace it with a real token from [@BotFather](https://t.me/BotFather). Load it from an environment variable or a file inside `tokens/` (already `.gitignore`d):

```python
import os
token = os.environ["TELEGRAM_BOT_TOKEN"]
```

## Conventions

- **Handlers**: must be `async def` accepting `(update, context)`.
- **Service functions**: return psutil objects or primitives; handlers are responsible for formatting output.
- **No module-level side effects**: service modules must only define functions, never call them at import time.
- **psutil imports**: import specific names from `psutil` (not the whole module), following the pattern in `monitor.py`.

## Known Issues

- **`heap_infomation.py`**: filename typo, imports `heap_info` which does not exist in psutil, and calls it at module level — raises `ImportError` on import. Do not import this file.
- **Legacy stubs**: `cpu_info.py`, `disks_info.py`, `network_info.py`, `process_management.py`, `sensors_info.py`, `users_info.py`, and `memory_info.py` are superseded by `monitor.py`.
- **`main.py` unused imports**: `logging`, `pathlib`, and `os` are imported but never used.

## Git Workflow

- Main development branch: `zoltraak` (on origin).
- Feature branches: `claude/<description>-<id>` pattern.
- **Commit messages are written in Spanish** (established by existing history).
- Always commit `uv.lock` alongside `pyproject.toml` changes.
