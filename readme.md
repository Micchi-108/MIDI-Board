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

## Silly project?
I  was thinking about doing something like this for a long time,
ever since I got my hands on an Audio Interface and Neural DSP.
I thought it's stupid to just click to turn off an effect in NDSP.
I searched for pedals and thought, "ehh, kinda of expensive.".
So this program was the result. It's vibecoded to just do my needs and I also find some
on reddit, asking for "using the actual computer keyboard".

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
