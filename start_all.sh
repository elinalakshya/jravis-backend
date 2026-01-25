#!/usr/bin/env bash

echo "🚀 Starting JRAVIS API"

export PYTHONPATH="$PWD:$PWD/src/src"

cd src/src
python -m uvicorn app:app --host 0.0.0.0 --port ${PORT:-10000}
