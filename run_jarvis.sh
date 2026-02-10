#!/bin/bash
# Launch Jarvis Eye
cd "$(dirname "$0")"
source jarvis_venv/bin/activate
python jarvis_eye.py
