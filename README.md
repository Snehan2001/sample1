# AI Robo Assistant

This workspace contains a Python-based voice assistant project with simple robot interactions such as greetings, time responses, jokes, and opening popular websites.

## Included scripts

- `robot.py` — text-based robot assistant
- `voice_robot.py` — voice-enabled assistant using microphone input
- `mic_test.py` — microphone check utility
- `test.py` — basic startup sanity check

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
2. Activate it:
   - Windows PowerShell:
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Run the assistant

```bash
python robot.py
```

Or for voice interaction:

```bash
python voice_robot.py
```

## Notes

- `pyaudio` may require system audio dependencies depending on your operating system.
- If microphone input is not working, check your audio device and drivers.
