# Jarvis Project

A voice-controlled AI desktop companion inspired by *Jarvis* from Iron Man. Features an animated floating arc reactor overlay and a voice interface that connects to a remote AI agent via WebSocket.

**macOS only** — uses native AppKit/Quartz for the transparent overlay window.

<p align="center">
  <img src="demo.gif" alt="Jarvis Demo" />
</p>

## How It Works

1. An animated arc reactor renders as a transparent always-on-top overlay (601 PNG frames at 30fps)
2. Hold **Right Command** to record audio from your mic
3. Speech is transcribed via Google Gemini STT
4. The transcription is sent to a remote agent (clawdbot) over an SSH-tunneled WebSocket
5. The agent's response is spoken back using Gemini TTS

## Setup

```bash
# Clone
git clone https://github.com/ilanp13/Jarvis_project.git
cd Jarvis_project

# Create venv and install deps
python3 -m venv jarvis_venv
source jarvis_venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your actual values
```

You also need:
- An SSH key configured for your remote server
- A Google Gemini API key
- The animation frames in `jarvis_frames_transparent/` (601 PNGs)

## Usage

```bash
# Eye animation only
./run_jarvis.sh

# Full system (eye + voice)
./run_jarvis_full.sh
```

**Controls:**
- Hold **Right Command** — record
- Release — send to agent & hear response
- **Escape** — quit

## Project Structure

```
jarvis_eye.py            # Animated transparent eye overlay (AppKit/Quartz)
jarvis_voice.py          # Simple text-based agent interface
jarvis_voice_full.py     # Full voice interface (STT -> Agent -> TTS)
run_jarvis.sh            # Launch eye only
run_jarvis_full.sh       # Launch eye + voice
jarvis_frames_transparent/  # Animation frames (not included in repo)
```

## Disclaimer

This project is provided **for educational and research purposes only**. The author assumes no responsibility or liability for any misuse, damage, or consequences arising from the use of this software. Use at your own risk. By using this project, you agree that the author is not responsible for any actions taken with it.

## License

MIT
