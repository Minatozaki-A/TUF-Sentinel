# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

**TUF-Sentinel** is a Telegram bot for system monitoring, written in Python. It exposes system metrics (CPU, memory, disk, network, processes, sensors, users) via Telegram commands using `psutil`.

The project is in early development: only `/hello` and `/memory` commands are fully implemented. The other service modules (`cpu_info`, `disks_info`, `network_info`, etc.) have psutil imports but no functions yet.

## Environment

This project uses [uv](https://docs.astral.sh/uv/) for dependency management and requires **Python >= 3.13**.

```bash
# Install dependencies
uv sync

# Run the bot
uv run main.py

# Add a dependency
uv add <package>
```

## Dependencies

Declared in `pyproject.toml`:
- `psutil >= 7.2.2` — system and process metrics
- `python-telegram-bot >= 22.7` — Telegram Bot API wrapper (async)

Transitive (locked in `uv.lock`): `httpx`, `anyio`, `certifi`, `h11`, `httpcore`, `idna`.

## Project Structure

```
TUF-Sentinel/
├── main.py                    # Bot entry point: command handlers, app startup
├── pyproject.toml             # Project metadata and dependencies
├── uv.lock                    # Locked dependency versions (commit this)
├── CLAUDE.md                  # This file
├── README.md                  # Minimal project header
└── services/                  # System monitoring modules (psutil wrappers)
    ├── memory_info.py         # IMPLEMENTED: virtual & swap memory
    ├── cpu_info.py            # Imports only — no functions yet
    ├── disks_info.py          # Imports only — no functions yet
    ├── network_info.py        # Imports only — no functions yet
    ├── process_management.py  # Imports only — no functions yet
    ├── sensors_info.py        # Imports only — no functions yet
    ├── users_info.py          # Imports only — no functions yet
    └── heap_infomation.py     # Stub with side-effecting import (see known issues)
```

## Architecture

- `main.py` registers async command handlers on a `telegram.ext.Application` and runs polling.
- Each Telegram command (`/hello`, `/memory`) maps to an `async def` handler that sends a reply.
- Service modules in `services/` expose plain Python functions returning formatted strings; handlers call these functions and forward the result to the user.
- No database, no config file, no web server — pure Telegram polling bot.

## Bot Token

The bot token is currently hardcoded as the string `"Token"` in `main.py`. **Before running**, replace it with a real token from [@BotFather](https://t.me/BotFather). The recommended approach is to load it from an environment variable or a secrets file excluded by `.gitignore` (the `tokens/` directory is already ignored).

```python
import os
token = os.environ["TELEGRAM_BOT_TOKEN"]
```

## Conventions

- **Async handlers**: all Telegram command handlers must be `async def` and accept `(update, context)` as parameters.
- **Service functions**: return a plain formatted string; let the handler do `await update.message.reply_text(result)`.
- **No side effects on import**: service modules must only define functions — do not call functions at module level (see `heap_infomation.py` known issue).
- **psutil usage**: import specific names from `psutil` rather than the whole module, matching the pattern in existing service files.

## Implementing a New Command

1. Add the monitoring function(s) to the appropriate file in `services/`.
2. Import the function in `main.py`.
3. Write an `async def <name>_handler(update, context)` that calls the function and replies.
4. Register the handler: `app.add_handler(CommandHandler("<command>", <name>_handler))`.

## Known Issues

- **`heap_infomation.py`**: filename has a typo ("infomation") and calls `heap_info()` at import time — this will raise a `NameError` on import since `heap_info` is not defined. Do not import this module until it is fixed.
- **Hardcoded token**: `main.py` uses the literal string `"Token"` — the bot will not connect until replaced.
- **Incomplete service modules**: `cpu_info`, `disks_info`, `network_info`, `process_management`, `sensors_info`, `users_info` contain only psutil imports with no implemented functions.
- **Unused import**: `memory_info.py` imports `logging` but does not use it.

## Git Workflow

- The main development branch is `zoltraak` (on origin).
- Feature/task branches follow the pattern `claude/<description>-<id>`.
- Commit messages are in Spanish (established by existing history).
- Always commit `uv.lock` alongside `pyproject.toml` changes.
