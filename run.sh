#!/usr/bin/env bash
set -euo pipefail

# Simple helper to create a venv, install deps and run the bot.
# Usage: ./run.sh

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

if [ ! -f .env ]; then
  cp .env.sample .env
  echo "Created .env from .env.sample — edit it and add DISCORD_TOKEN before running for real."
fi

PYTHON=${PYTHON:-python}
VENV_DIR=.venv

if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtualenv in $VENV_DIR"
  "$PYTHON" -m venv "$VENV_DIR"
fi

PIP="$VENV_DIR/bin/pip"
PY="$VENV_DIR/bin/python"

echo "Installing requirements (this may take a minute)..."
"$PIP" install -U pip
"$PIP" install -r requirements.txt

echo "Starting bot..."
"$PY" bot.py
