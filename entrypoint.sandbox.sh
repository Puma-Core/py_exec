#!/bin/bash
set -e

echo "Running entrypoint script for sandbox environment"

echo "Installing dependencies..."
apt-get update
apt-get install -y python3 python3-venv curl

if command -v apt &> /dev/null; then
    apt install socat
fi

if [ ! -d ".venv" ]; then
    echo "Creating virtual environment at .venv"
    python3 -m venv .venv
    echo "Virtual environment created."
fi

echo "Activating virtual environment..."
. .venv/bin/activate
echo "Virtual environment activated. ✓"

echo "Checking Microsandbox installation..."
/root/.local/bin/msb --version

mkdir -p /tmp/sandbox-workspace

echo "Starting Microsandbox server on localhost:5555..."
cd /tmp/sandbox-workspace
/root/.local/bin/msb server start --port 5555 --dev --path /tmp/sandbox-workspace &
MSB_PID=$!

echo "Waiting for Microsandbox to start..."
for i in {1..30}; do
    if curl -s -f http://127.0.0.1:5555/api/v1/health >/dev/null 2>&1; then
        echo "Microsandbox is ready on port 5555!"
        break
    fi
    echo "Attempt $i/30 - waiting for Microsandbox..."
    sleep 2
done

if ! curl -s -f http://127.0.0.1:5555/api/v1/health >/dev/null 2>&1; then
    echo "ERROR: Microsandbox failed to start!"
    kill $MSB_PID 2>/dev/null || true
    exit 1
fi

echo "Starting proxy from 0.0.0.0:5556 to 127.0.0.1:5555..."
exec socat TCP-LISTEN:5556,fork,reuseaddr,bind=0.0.0.0 TCP:127.0.0.1:5555