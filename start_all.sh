#!/usr/bin/env bash

echo "🚀 Starting JRAVIS API"

set -a
source .env
set +a

export PYTHONPATH="$PWD:$PWD/src/src"

cd src/src
python -m uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}

