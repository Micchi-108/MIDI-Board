## MIDI Board

A configurable MIDI pedalboard controller for Windows.

## Features

- MIDI CC messages
- MIDI Note messages
- MIDI Program Change messages
- Configurable MIDI channels
- Momentary and toggle modes
- Configurable on/off values
- Editable pedal labels
- MIDI port selection
- Keyboard mapping
- Configurable pedal settings through JSON

## Requirements

- Windows
- Python 3.12
- A MIDI device or virtual MIDI port

Python dependencies:

- mido
- python-rtmidi
- keyboard

## Configuration

Pedal settings are stored in `pedals.json`.

Application settings are stored in `settings.json`.

## Running from source

Install the required packages:

```bash
pip install -r requirements.txt