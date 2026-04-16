# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

A Telegram bot written in Python, currently in early development.

## Environment

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

```bash
# Install dependencies
uv sync

# Run the bot
uv run main.py

# Add a dependency
uv add <package>
```

## Dependencies

- Python >= 3.13
- `python-telegram-bot` is imported in `main.py` (`import telegram`) but not yet declared in `pyproject.toml` — add it with `uv add python-telegram-bot` before running.
