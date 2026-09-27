## ⚠️⚠️ Just a Notice ⚠️⚠️

Building from source does not guarantee that Windows Smart App Control will allow the resulting executable to run. 
PyInstaller-generated executables are not automatically code-signed, so Windows may still display a security warning or block the application depending on the user's security configuration.


If you are comfortable running Python code and want to verify the application yourself, you can build the executable locally from the source code. 
This allows you to inspect the source and create the executable yourself, but it does not automatically give the resulting executable a Microsoft-trusted reputation.


# MIDI Board

A (vibecoded) configurable MIDI pedalboard controller for Windows.

## Features

* MIDI CC messages
* MIDI Note messages
* MIDI Program Change messages
* Configurable MIDI channels
* Momentary and toggle modes
* Configurable on/off values
* Editable pedal labels
* MIDI port selection
* Keyboard mapping
* Configurable pedal settings through JSON

## Silly project?

I was thinking about doing something like this for a long time, ever since I got my hands on an audio interface and Neural DSP.
I thought it was tedious to have to use a mouse just to turn an effect on or off in NDSP. 
Looked into MIDI pedals, but thought, "ehh, kinda expensive."
So this is how this program was made.

It's vibecoded to do what I need, and also found posts on Reddit asking about using the actual computer keyboard as a MIDI controller. So I thought, why not make something like that?

## Requirements

* Windows
* Python 3.12 (only required if running from source)
* A MIDI device or virtual MIDI port

### Python dependencies

* mido
* python-rtmidi
* keyboard

## Configuration

Pedal settings are stored in `pedals.json`.

Application settings are stored in `settings.json`.

## Running from source

Install the required packages:

```bash
pip install -r requirements.txt
```

Then run:

```bash
python gui.py
```

## Windows Release

A standalone Windows executable is available in the **Releases** section.

The release ZIP contains:

* `MIDI Board.exe`
* `pedals.json`
* `settings.json`

Python does not need to be installed to use the standalone executable.

## ⚠️⚠️ Windows SmartScreen Warning ⚠️⚠️

Because  MIDI Board is a small, independently distributed application and the Windows executable is not currently code-signed, Windows SmartScreen may display a warning when you first run it.

If you downloaded the application from the project's official GitHub Releases page and have verified that it is the correct release, you can proceed as follows:

1. Extract the downloaded ZIP.
2. Open the extracted folder.
3. Run `MIDI Board.exe`.
4. If Windows displays **"Windows protected your PC"**, click **More info**.
5. Windows should then show additional information about the application.
6. If you have verified that you downloaded the correct release, you can choose **Run anyway**.

Do not disable Windows Defender or other Windows security features globally just to run the application.

If you are unsure about a security warning or where the file came from, do not run it.

## ⚠️⚠️ Windows Smart App Control ⚠️⚠️

Some Windows 11 systems have Smart App Control enabled. Unlike the normal SmartScreen prompt, Smart App Control may block the application entirely because the executable is not currently code-signed or recognized by Microsoft's reputation system.

If Smart App Control blocks Mik MIDI Board, you may see a message indicating that Windows prevented an untrusted or unknown application from running.

[!IMPORTANT]
Do not disable Smart App Control or Windows security features just to run Mik MIDI Board.

If Windows blocks the application, you can instead:

Verify that you downloaded the ZIP from the official GitHub Releases page.
Check that the files have not been modified or replaced.
Build the application yourself from the source code if you want to verify the build process.

If you are unsure about where the application came from or why Windows is blocking it, do not run it.

The application is currently distributed without a commercial code-signing certificate, so these warnings are expected on some Windows systems.


## Building from source

If you would rather build the executable yourself, you can download the source code from this repository.

You'll need:

* Windows
* Python 3.12

Install the dependencies:

```bash
pip install -r requirements.txt
```

Install PyInstaller:

```bash
pip install pyinstaller
```

Then build the executable:

```bash
py -3.12 -m PyInstaller --onefile --windowed --clean --name "MIDI Board" --collect-all rtmidi --hidden-import=mido.backends.rtmidi gui.py
```

The resulting executable will be placed in the `dist` folder.

After building, place the executable together with:

```text
pedals.json
settings.json
```

The three files should be kept in the same folder when running the application.

You can rename the generated executable to:

```text
MIDI Board.exe
```

Building from source is completely optional. The official Windows release already contains a standalone executable.
