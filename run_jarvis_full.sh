#!/bin/bash
# Launch Jarvis Eye with Full Voice Interface
cd "$(dirname "$0")"

# Load environment variables from .env if present
if [ -f .env ]; then
    set -a
    source .env
    set +a
fi

JARVIS_VPS_HOST="${JARVIS_VPS_HOST:?Error: JARVIS_VPS_HOST not set. Copy .env.example to .env and fill in your values.}"
JARVIS_SSH_TUNNEL_PORT="${JARVIS_SSH_TUNNEL_PORT:-18790}"

echo "=================================="
echo "  Starting Jarvis Eye + Voice"
echo "=================================="
echo ""

# Check if SSH tunnel is already running
if ! pgrep -f "ssh.*${JARVIS_SSH_TUNNEL_PORT}.*${JARVIS_VPS_HOST}" > /dev/null; then
    echo "Starting SSH tunnel..."
    ssh -f -N -L "${JARVIS_SSH_TUNNEL_PORT}:127.0.0.1:18789" "root@${JARVIS_VPS_HOST}"
    sleep 2
    echo "SSH tunnel connected"
else
    echo "SSH tunnel already running"
fi

# Activate virtual environment
source jarvis_venv/bin/activate

# Kill any existing Jarvis Eye
pkill -f jarvis_eye.py 2>/dev/null

# Start Jarvis Eye animation in background
echo "Starting Jarvis Eye animation..."
python jarvis_eye.py &
EYE_PID=$!

# Give the eye time to load frames
echo "  Loading frames..."
sleep 5
echo "Jarvis Eye running"
echo ""

# Start full voice interface
echo "Starting voice interface..."
echo ""
python jarvis_voice_full.py

# Cleanup
echo ""
echo "Stopping Jarvis Eye..."
kill $EYE_PID 2>/dev/null
echo "Done."
