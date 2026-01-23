#!/usr/bin/env bash

echo "🚀 Starting JRAVIS API + WORKER"

# Make both root and src/src importable
export PYTHONPATH="$PWD:$PWD/src/src"

# Start API in background
cd src/src
python -m uvicorn app:app --host 0.0.0.0 --port $PORT &

# Back to project root
cd ../..

# Start worker (foreground)
python worker.py
