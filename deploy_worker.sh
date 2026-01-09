#!/usr/bin/env bash
set -e

echo "🚀 Deploying JRAVIS Worker (Replit Stable Mode)..."

cd jravis-worker || exit 1

echo "🔄 Syncing worker repo..."
git fetch origin
git reset --hard origin/main

echo "🐍 Python version:"
python3 --version

echo "🔥 Starting JRAVIS worker (no pip, no venv)..."
exec python3 worker.py