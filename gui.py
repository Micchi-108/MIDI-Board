import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import keyboard
import mido


JSON_FILE = "pedals.json"
SETTINGS_FILE = "settings.json"


DEFAULT_PEDALS = {
    "1": {"type": "cc", "number": 1, "channel": 1, "mode": "momentary", "on_value": 127, "off_value": 0},
    "2": {"type": "cc", "number": 2, "channel": 1, "mode": "momentary", "on_value": 127, "off_value": 0},
    "3": {"type": "cc", "number": 3, "channel": 1, "mode": "momentary", "on_value": 127, "off_value": 0},
    "4": {"type": "cc", "number": 4, "channel": 1, "mode": "momentary", "on_value": 127, "off_value": 0},
    "5": {"type": "cc", "number": 5, "channel": 1, "mode": "momentary", "on_value": 127, "off_value": 0},
    "6": {"type": "cc", "number": 6, "channel": 1, "mode": "momentary", "on_value": 127, "off_value": 0},
    "7": {"type": "cc", "number": 7, "channel": 1, "mode": "momentary", "on_value": 127, "off_value": 0},
    "8": {"type": "cc", "number": 8, "channel": 1, "mode": "momentary", "on_value": 127, "off_value": 0},
    "9": {"type": "cc", "number": 9, "channel": 1, "mode": "momentary", "on_value": 127, "off_value": 0},
    "0": {"type": "cc", "number": 10, "channel": 1, "mode": "momentary", "on_value": 127, "off_value": 0},

    "q": {"type": "cc", "number": 11, "channel": 1, "mode": "momentary", "on_value": 127, "off_value": 0},
    "w": {"type": "cc", "number": 12, "channel": 1, "mode": "momentary", "on_value": 127, "off_value": 0},
    "e": {"type": "cc", "number": 13, "channel": 1, "mode": "momentary", "on_value": 127, "off_value": 0},
    "r": {"type": "cc", "number": 14, "channel": 1, "mode": "momentary", "on_value": 127, "off_value": 0},
    "t": {"type": "cc", "number": 15, "channel": 1, "mode": "momentary", "on_value": 127, "off_value": 0},
    "y": {"type": "cc", "number": 16, "channel": 1, "mode": "momentary", "on_value": 127, "off_value": 0},
    "u": {"type": "cc", "number": 17, "channel": 1, "mode": "momentary", "on_value": 127, "off_value": 0},
    "i": {"type": "cc", "number": 18, "channel": 1, "mode": "momentary", "on_value": 127, "off_value": 0},
    "o": {"type": "cc", "number": 19, "channel": 1, "mode": "momentary", "on_value": 127, "off_value": 0},
    "p": {"type": "cc", "number": 20, "channel": 1, "mode": "momentary", "on_value": 127, "off_value": 0},

    "a": {"type": "cc", "number": 21, "channel": 1, "mode": "momentary", "on_value": 127, "off_value": 0},
    "s": {"type": "cc", "number": 22, "channel": 1, "mode": "momentary", "on_value": 127, "off_value": 0},
    "d": {"type": "cc", "number": 23, "channel": 1, "mode": "momentary", "on_value": 127, "off_value": 0},
    "f": {"type": "cc", "number": 24, "channel": 1, "mode": "momentary", "on_value": 127, "off_value": 0},
    "g": {"type": "cc", "number": 25, "channel": 1, "mode": "momentary", "on_value": 127, "off_value": 0},
    "h": {"type": "cc", "number": 26, "channel": 1, "mode": "momentary", "on_value": 127, "off_value": 0},
    "j": {"type": "cc", "number": 27, "channel": 1, "mode": "momentary", "on_value": 127, "off_value": 0},
    "k": {"type": "cc", "number": 28, "channel": 1, "mode": "momentary", "on_value": 127, "off_value": 0},
    "l": {"type": "cc", "number": 29, "channel": 1, "mode": "momentary", "on_value": 127, "off_value": 0},

    "z": {"type": "cc", "number": 30, "channel": 1, "mode": "momentary", "on_value": 127, "off_value": 0},
    "x": {"type": "cc", "number": 31, "channel": 1, "mode": "momentary", "on_value": 127, "off_value": 0},
    "c": {"type": "cc", "number": 32, "channel": 1, "mode": "momentary", "on_value": 127, "off_value": 0},
    "v": {"type": "cc", "number": 33, "channel": 1, "mode": "momentary", "on_value": 127, "off_value": 0},
    "b": {"type": "cc", "number": 34, "channel": 1, "mode": "momentary", "on_value": 127, "off_value": 0},
    "n": {"type": "cc", "number": 35, "channel": 1, "mode": "momentary", "on_value": 127, "off_value": 0},
    "m": {"type": "cc", "number": 36, "channel": 1, "mode": "momentary", "on_value": 127, "off_value": 0},

    "space": {
        "type": "note",
        "number": 60,
        "channel": 1,
        "mode": "momentary",
        "on_value": 127,
        "off_value": 0
    }
}


# --------------------------------------------------
# LOAD / SAVE
# --------------------------------------------------

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return {
            "midi_port": ""
        }

    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, dict):
            return data

    except Exception as error:
        print("Settings Load Error:", error)

    return {
        "midi_port": ""
    }


def save_settings():
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
            json.dump(
                settings,
                file,
                indent=4
            )

    except Exception as error:
        print("Settings Save Error:", error)


settings = load_settings()


def load_pedals():
    if not os.path.exists(JSON_FILE):
        return {
            key: value.copy()
            for key, value in DEFAULT_PEDALS.items()
        }

    try:
        with open(JSON_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, dict):
            return data

    except Exception as error:
        messagebox.showerror(
            "Load Error",
            f"Could not load {JSON_FILE}:\n\n{error}"
        )

    return {
        key: value.copy()
        for key, value in DEFAULT_PEDALS.items()
    }


pedals = load_pedals()


def save_pedals():
    try:
        with open(JSON_FILE, "w", encoding="utf-8") as file:
            json.dump(
                pedals,
                file,
                indent=4
            )

        info_var.set(
            "PEDALBOARD SAVED."
        )

        root.after(
            1500,
            update_status
        )

    except Exception as error:
        messagebox.showerror(
            "Save Error",
            f"Could not save {JSON_FILE}:\n\n{error}"
        )


# --------------------------------------------------
# GLOBAL STATE
# --------------------------------------------------

port = None
engine_running = False
toggle_states = {}
pressed_keys = set()
keyboard_locked = True
pedal_editor = None
editor_key = None
editor_key_label = None
editor_type_var = None
editor_number_var = None
editor_channel_var = None
editor_mode_var = None
editor_on_value_var = None
editor_off_value_var = None
editor_label_var = None
editor_dsp_var = None


# --------------------------------------------------
# COLORS
# --------------------------------------------------

BG = "#151515"
PANEL = "#202020"
PAD = "#292929"
PAD_ASSIGNED = "#3a3a3a"
PAD_HOVER = "#454545"
PAD_ACTIVE = "#777777"
TEXT = "#eeeeee"
SUBTEXT = "#999999"
GREEN = "#55dd88"
RED = "#dd6666"


# --------------------------------------------------
# MIDI PORTS
# --------------------------------------------------

def get_midi_ports():
    try:
        return mido.get_output_names()

    except Exception as error:
        print(
            "MIDI Port Detection Error:",
            error
        )

        return []


def update_midi_info():

    selected = midi_port_var.get()

    if selected:

        midi_info.config(
            text=f"MIDI: {selected}"
        )

    else:

        midi_info.config(
            text="MIDI: No output port detected"
        )


def refresh_midi_ports():

    if engine_running:

        messagebox.showinfo(
            "Engine Running",
            "Stop the engine before changing MIDI ports."
        )

        return

    ports = get_midi_ports()

    midi_combo["values"] = ports

    saved_port = settings.get(
        "midi_port",
        ""
    )

    if saved_port in ports:

        midi_combo.set(
            saved_port
        )

    elif ports:

        midi_combo.set(
            ports[0]
        )

    else:

        midi_combo.set(
            ""
        )

    update_midi_info()


def midi_port_selected(event=None):

    selected = midi_port_var.get()

    if selected:

        settings["midi_port"] = selected

        save_settings()

    update_midi_info()


# --------------------------------------------------
# MIDI SEND
# --------------------------------------------------

def send_midi(
    pedal,
    pressed=True
):

    global port

    if port is None:
        return

    pedal_type = pedal.get(
        "type",
        "cc"
    )

    number = int(
        pedal.get(
            "number",
            0
        )
    )

    channel = int(
        pedal.get(
            "channel",
            1
        )
    ) - 1

    on_value = int(
        pedal.get(
            "on_value",
            127
        )
    )

    off_value = int(
        pedal.get(
            "off_value",
            0
        )
    )

    try:

        if pedal_type == "cc":

            value = (
                on_value
                if pressed
                else off_value
            )

            port.send(
                mido.Message(
                    "control_change",
                    channel=channel,
                    control=number,
                    value=value
                )
            )

        elif pedal_type == "note":

            if pressed:

                port.send(
                    mido.Message(
                        "note_on",
                        channel=channel,
                        note=number,
                        velocity=on_value
                    )
                )

            else:

                port.send(
                    mido.Message(
                        "note_off",
                        channel=channel,
                        note=number,
                        velocity=off_value
                    )
                )

        elif pedal_type == "pc":

            if pressed:

                port.send(
                    mido.Message(
                        "program_change",
                        channel=channel,
                        program=number
                    )
                )

    except Exception as error:

        print(
            "MIDI Error:",
            error
        )


def send_off(pedal):

    send_midi(
        pedal,
        False
    )


# --------------------------------------------------
# PEDAL ENGINE
# --------------------------------------------------

def pedal_press(event):

    if not engine_running:
        return

    key = event.name

    if key not in pedals:
        return

    pedal = pedals[key]

    if key in pressed_keys:
        return

    pressed_keys.add(key)

    pedal_type = pedal.get(
        "type",
        "cc"
    )

    mode = pedal.get(
        "mode",
        "momentary"
    )

    if pedal_type == "pc":

        send_midi(
            pedal,
            True
        )

        update_pad_visual(
            key,
            True
        )

        return

    if mode == "momentary":

        send_midi(
            pedal,
            True
        )

        update_pad_visual(
            key,
            True
        )

    elif mode == "toggle":

        current = toggle_states.get(
            key,
            False
        )

        new_state = not current

        toggle_states[key] = new_state

        send_midi(
            pedal,
            new_state
        )

        update_pad_visual(
            key,
            new_state
        )


def pedal_release(event):

    if not engine_running:
        return

    key = event.name

    if key not in pedals:
        return

    pedal = pedals[key]

    if key not in pressed_keys:
        return

    pressed_keys.discard(
        key
    )

    pedal_type = pedal.get(
        "type",
        "cc"
    )

    mode = pedal.get(
        "mode",
        "momentary"
    )

    if pedal_type == "pc":

        update_pad_visual(
            key,
            False
        )

        return

    if mode == "momentary":

        send_midi(
            pedal,
            False
        )

        update_pad_visual(
            key,
            False
        )

    elif mode == "toggle":

        update_pad_visual(
            key,
            toggle_states.get(
                key,
                False
            )
        )


# --------------------------------------------------
# KEYBOARD HOOKS / LOCK
# --------------------------------------------------

def install_keyboard_hooks():

    keyboard.unhook_all()

    for key in pedals:

        keyboard.on_press_key(
            key,
            pedal_press,
            suppress=keyboard_locked
        )

        keyboard.on_release_key(
            key,
            pedal_release,
            suppress=keyboard_locked
        )


def update_keyboard_lock_ui():

    if keyboard_locked:

        keyboard_lock_button.config(
            text="🔒 KEYBOARD LOCK ON",
            bg=GREEN,
            fg=BG,
            activebackground=GREEN,
            activeforeground=BG
        )

        keyboard_lock_status.config(
            text="● LOCKED",
            fg=GREEN
        )

    else:

        keyboard_lock_button.config(
            text="🔓 KEYBOARD LOCK OFF",
            bg="#333333",
            fg=TEXT,
            activebackground="#444444",
            activeforeground=TEXT
        )

        keyboard_lock_status.config(
            text="● UNLOCKED",
            fg=RED
        )


def toggle_keyboard_lock():

    global keyboard_locked

    keyboard_locked = not keyboard_locked

    if engine_running:

        # Rebuild the hooks so the new suppress setting takes effect.
        install_keyboard_hooks()

        # Do not let a key that was physically held during the
        # hook rebuild get stuck in the pressed state.
        pressed_keys.clear()

    update_keyboard_lock_ui()


# --------------------------------------------------
# ENGINE START / STOP
# --------------------------------------------------

def start_engine():

    global port
    global engine_running

    if engine_running:
        return

    selected_port = midi_port_var.get()

    if not selected_port:

        messagebox.showerror(
            "MIDI Error",
            "No MIDI output port is selected."
        )

        return

    try:

        port = mido.open_output(
            selected_port
        )

    except Exception as error:

        messagebox.showerror(
            "MIDI Error",
            f"Could not open MIDI port:\n\n"
            f"{selected_port}\n\n"
            f"{error}"
        )

        port = None

        return

    engine_running = True

    pressed_keys.clear()
    toggle_states.clear()

    install_keyboard_hooks()

    update_status()

    info_var.set(
        f"ENGINE RUNNING. MIDI → {selected_port}"
    )


def stop_engine():

    global port
    global engine_running

    if not engine_running:
        return

    # Stop accepting pedal events first.
    engine_running = False

    # Remove ALL keyboard hooks created by this application.
    # This prevents mapped keys from remaining suppressed
    # after the engine is turned off.
    keyboard.unhook_all()

    # Send OFF messages for any pedals that were still held
    # when the engine was stopped.
    for key in list(pressed_keys):

        pedal = pedals.get(
            key
        )

        if pedal:

            send_off(
                pedal
            )

    pressed_keys.clear()
    toggle_states.clear()

    if port:

        try:

            port.close()

        except Exception:
            pass

        port = None

    reset_pad_visuals()

    update_status()

    info_var.set(
        "ENGINE STOPPED."
    )


def toggle_engine():

    if engine_running:

        stop_engine()

    else:

        start_engine()


# --------------------------------------------------
# STATUS
# --------------------------------------------------

def update_status():

    if engine_running:

        status.config(
            text="● ENGINE RUNNING",
            fg=GREEN
        )

        engine_button.config(
            text="● ENGINE ON"
        )

    else:

        status.config(
            text="● ENGINE OFF",
            fg=RED
        )

        engine_button.config(
            text="○ ENGINE OFF"
        )


# --------------------------------------------------
# PAD VISUALS
# --------------------------------------------------

pad_buttons = {}


def update_pad_visual(
    key,
    active
):

    button = pad_buttons.get(
        key
    )

    if button is None:
        return

    if active:

        button.config(
            bg=PAD_ACTIVE,
            relief="sunken"
        )

    else:

        pedal = pedals.get(
            key,
            {}
        )

        if (
            pedal.get("label")
            or pedal.get("dsp_parameter")
        ):

            button.config(
                bg=PAD_ASSIGNED,
                relief="raised"
            )

        else:

            button.config(
                bg=PAD,
                relief="raised"
            )


def reset_pad_visuals():

    for key in pad_buttons:

        update_pad_visual(
            key,
            False
        )


# --------------------------------------------------
# INDIVIDUAL PEDAL EDITOR
# --------------------------------------------------

def edit_pedal(key):

    global pedal_editor
    global editor_key
    global editor_key_label
    global editor_type_var
    global editor_number_var
    global editor_channel_var
    global editor_mode_var
    global editor_on_value_var
    global editor_off_value_var
    global editor_label_var
    global editor_dsp_var

    if engine_running:

        messagebox.showinfo(
            "Engine Running",
            "Stop the engine before editing a pedal."
        )

        return

    # --------------------------------------------------
    # SAVE THE CURRENT KEY BEFORE SWITCHING
    # --------------------------------------------------

    def save_current_editor(show_message=False):

        if not editor_key:
            return True

        try:

            number = int(editor_number_var.get())
            channel = int(editor_channel_var.get())
            on_value = int(editor_on_value_var.get())
            off_value = int(editor_off_value_var.get())

        except ValueError:

            messagebox.showerror(
                "Invalid Value",
                "Number, Channel, On Value and Off Value must be numbers.",
                parent=pedal_editor
            )

            return False

        if not 0 <= number <= 127:

            messagebox.showerror(
                "Invalid Number",
                "MIDI number must be between 0 and 127.",
                parent=pedal_editor
            )

            return False

        if not 1 <= channel <= 16:

            messagebox.showerror(
                "Invalid Channel",
                "MIDI channel must be between 1 and 16.",
                parent=pedal_editor
            )

            return False

        if not 0 <= on_value <= 127:

            messagebox.showerror(
                "Invalid On Value",
                "On Value must be between 0 and 127.",
                parent=pedal_editor
            )

            return False

        if not 0 <= off_value <= 127:

            messagebox.showerror(
                "Invalid Off Value",
                "Off Value must be between 0 and 127.",
                parent=pedal_editor
            )

            return False

        new_pedal = {
            "type": editor_type_var.get(),
            "number": number,
            "channel": channel,
            "mode": editor_mode_var.get(),
            "on_value": on_value,
            "off_value": off_value
        }

        label = editor_label_var.get().strip()
        dsp = editor_dsp_var.get().strip()

        if label:
            new_pedal["label"] = label

        if dsp:
            new_pedal["dsp_parameter"] = dsp

        pedals[editor_key] = new_pedal

        rebuild_board()
        save_pedals()

        if show_message:
            info_var.set(
                f"PEDAL {editor_key.upper()} SAVED."
            )

        return True

    # --------------------------------------------------
    # LOAD A KEY INTO THE EXISTING EDITOR
    # --------------------------------------------------

    def load_editor_key(new_key):

        global editor_key

        # If another key is already being edited, save it first.
        if editor_key is not None and editor_key != new_key:

            if not save_current_editor():
                return

        editor_key = new_key

        pedal = pedals.get(
            new_key,
            {}
        )

        editor_type_var.set(
            pedal.get("type", "cc")
        )

        editor_number_var.set(
            str(pedal.get("number", 0))
        )

        editor_channel_var.set(
            str(pedal.get("channel", 1))
        )

        editor_mode_var.set(
            pedal.get("mode", "momentary")
        )

        editor_on_value_var.set(
            str(pedal.get("on_value", 127))
        )

        editor_off_value_var.set(
            str(pedal.get("off_value", 0))
        )

        editor_label_var.set(
            pedal.get("label", "")
        )

        editor_dsp_var.set(
            pedal.get("dsp_parameter", "")
        )

        pedal_editor.title(
            f"Edit Pedal: {new_key.upper()}"
        )

        editor_key_label.config(
            text=f"KEY: {new_key.upper()}"
        )

        pedal_editor.deiconify()
        pedal_editor.lift()
        pedal_editor.focus_force()

    # --------------------------------------------------
    # CREATE THE EDITOR ONLY ONCE
    # --------------------------------------------------

    if pedal_editor is not None and pedal_editor.winfo_exists():

        load_editor_key(key)
        return

    pedal_editor = tk.Toplevel(root)
    pedal_editor.title(f"Edit Pedal: {key.upper()}")
    pedal_editor.geometry("400x470")
    pedal_editor.configure(bg=BG)
    pedal_editor.resizable(False, False)

    pedal_editor.columnconfigure(1, weight=1)

    editor_key_label = tk.Label(
        pedal_editor,
        text=f"KEY: {key.upper()}",
        bg=BG,
        fg=GREEN,
        font=("Segoe UI", 14, "bold")
    )
    editor_key_label.grid(
        row=0,
        column=0,
        columnspan=2,
        pady=(15, 10)
    )

    editor_type_var = tk.StringVar()
    editor_number_var = tk.StringVar()
    editor_channel_var = tk.StringVar()
    editor_mode_var = tk.StringVar()
    editor_on_value_var = tk.StringVar()
    editor_off_value_var = tk.StringVar()
    editor_label_var = tk.StringVar()
    editor_dsp_var = tk.StringVar()

    def add_field(label, variable, row):

        tk.Label(
            pedal_editor,
            text=label,
            bg=BG,
            fg=TEXT,
            anchor="w"
        ).grid(
            row=row,
            column=0,
            padx=15,
            pady=7,
            sticky="w"
        )

        entry = tk.Entry(
            pedal_editor,
            textvariable=variable,
            bg=PANEL,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat"
        )

        entry.grid(
            row=row,
            column=1,
            padx=15,
            pady=7,
            sticky="ew"
        )

        return entry

    tk.Label(
        pedal_editor,
        text="Type",
        bg=BG,
        fg=TEXT,
        anchor="w"
    ).grid(row=1, column=0, padx=15, pady=7, sticky="w")

    type_combo = ttk.Combobox(
        pedal_editor,
        textvariable=editor_type_var,
        values=["cc", "note", "pc"],
        state="readonly"
    )
    type_combo.grid(row=1, column=1, padx=15, pady=7, sticky="ew")

    add_field("Number", editor_number_var, 2)
    add_field("Channel", editor_channel_var, 3)

    tk.Label(
        pedal_editor,
        text="Mode",
        bg=BG,
        fg=TEXT,
        anchor="w"
    ).grid(row=4, column=0, padx=15, pady=7, sticky="w")

    mode_combo = ttk.Combobox(
        pedal_editor,
        textvariable=editor_mode_var,
        values=["momentary", "toggle"],
        state="readonly"
    )
    mode_combo.grid(row=4, column=1, padx=15, pady=7, sticky="ew")

    add_field("On Value", editor_on_value_var, 5)
    add_field("Off Value", editor_off_value_var, 6)
    add_field("Pad Label", editor_label_var, 7)
    add_field("DSP Parameter", editor_dsp_var, 8)

    button_frame = tk.Frame(
        pedal_editor,
        bg=BG
    )
    button_frame.grid(
        row=10,
        column=0,
        columnspan=2,
        pady=20
    )

    tk.Button(
        button_frame,
        text="SAVE",
        width=12,
        command=lambda: save_current_editor(True),
        bg="#333333",
        fg=TEXT,
        activebackground="#444444",
        activeforeground=TEXT
    ).pack(side="left", padx=5)

    tk.Button(
        button_frame,
        text="CLOSE",
        width=12,
        command=lambda: close_editor(),
        bg="#333333",
        fg=TEXT,
        activebackground="#444444",
        activeforeground=TEXT
    ).pack(side="left", padx=5)

    def close_editor():

        global pedal_editor
        global editor_key

        if not save_current_editor():
            return

        pedal_editor.destroy()
        pedal_editor = None
        editor_key = None

    pedal_editor.protocol(
        "WM_DELETE_WINDOW",
        close_editor
    )

    load_editor_key(key)


# --------------------------------------------------
# BATCH EDITOR
# --------------------------------------------------

BATCH_ROWS = {
    "Row 1 (1-0)": [
        "1", "2", "3", "4", "5",
        "6", "7", "8", "9", "0"
    ],

    "Row 2 (Q-P)": [
        "q", "w", "e", "r", "t",
        "y", "u", "i", "o", "p"
    ],

    "Row 3 (A-L)": [
        "a", "s", "d", "f", "g",
        "h", "j", "k", "l"
    ],

    "Row 4 (Z-M)": [
        "z", "x", "c", "v",
        "b", "n", "m"
    ],

    "Space": [
        "space"
    ]
}


def batch_edit():

    if engine_running:

        messagebox.showinfo(
            "Engine Running",
            "Stop the engine before using Batch Edit."
        )

        return

    editor = tk.Toplevel(
        root
    )

    editor.title(
        "Batch Edit"
    )

    editor.geometry(
        "430x560"
    )

    editor.configure(
        bg=BG
    )

    editor.resizable(
        False,
        False
    )

    editor.columnconfigure(
        1,
        weight=1
    )

    # --------------------------------------------------
    # TITLE
    # --------------------------------------------------

    tk.Label(
        editor,
        text="BATCH EDIT",
        bg=BG,
        fg=GREEN,
        font=("Segoe UI", 16, "bold")
    ).grid(
        row=0,
        column=0,
        columnspan=2,
        pady=(18, 15)
    )

    # --------------------------------------------------
    # VARIABLES
    # --------------------------------------------------

    target_var = tk.StringVar(
        value="Row 1 (1-0)"
    )

    type_var = tk.StringVar(
        value="cc"
    )

    number_mode_var = tk.StringVar(
        value="Sequential"
    )

    number_var = tk.StringVar(
        value="1"
    )

    channel_var = tk.StringVar(
        value="1"
    )

    mode_var = tk.StringVar(
        value="momentary"
    )

    on_value_var = tk.StringVar(
        value="127"
    )

    off_value_var = tk.StringVar(
        value="0"
    )

    clear_metadata_var = tk.BooleanVar(
        value=False
    )

    # --------------------------------------------------
    # FIELD HELPER
    # --------------------------------------------------

    def add_label(
        text,
        row
    ):

        tk.Label(
            editor,
            text=text,
            bg=BG,
            fg=TEXT,
            anchor="w"
        ).grid(
            row=row,
            column=0,
            padx=18,
            pady=7,
            sticky="w"
        )

    # --------------------------------------------------
    # TARGET
    # --------------------------------------------------

    add_label(
        "Target",
        1
    )

    target_combo = ttk.Combobox(
        editor,
        textvariable=target_var,
        values=[
            "Entire Board",
            "Row 1 (1-0)",
            "Row 2 (Q-P)",
            "Row 3 (A-L)",
            "Row 4 (Z-M)",
            "Space"
        ],
        state="readonly"
    )

    target_combo.grid(
        row=1,
        column=1,
        padx=18,
        pady=7,
        sticky="ew"
    )

    # --------------------------------------------------
    # TYPE
    # --------------------------------------------------

    add_label(
        "Type",
        2
    )

    type_combo = ttk.Combobox(
        editor,
        textvariable=type_var,
        values=[
            "cc",
            "note",
            "pc"
        ],
        state="readonly"
    )

    type_combo.grid(
        row=2,
        column=1,
        padx=18,
        pady=7,
        sticky="ew"
    )

    # --------------------------------------------------
    # NUMBER MODE
    # --------------------------------------------------

    add_label(
        "Number Mode",
        3
    )

    number_mode_combo = ttk.Combobox(
        editor,
        textvariable=number_mode_var,
        values=[
            "Sequential",
            "Same Number"
        ],
        state="readonly"
    )

    number_mode_combo.grid(
        row=3,
        column=1,
        padx=18,
        pady=7,
        sticky="ew"
    )

    # --------------------------------------------------
    # START / NUMBER
    # --------------------------------------------------

    add_label(
        "Start / Number",
        4
    )

    number_entry = tk.Entry(
        editor,
        textvariable=number_var,
        bg=PANEL,
        fg=TEXT,
        insertbackground=TEXT,
        relief="flat"
    )

    number_entry.grid(
        row=4,
        column=1,
        padx=18,
        pady=7,
        sticky="ew"
    )

    # --------------------------------------------------
    # CHANNEL
    # --------------------------------------------------

    add_label(
        "Channel",
        5
    )

    channel_entry = tk.Entry(
        editor,
        textvariable=channel_var,
        bg=PANEL,
        fg=TEXT,
        insertbackground=TEXT,
        relief="flat"
    )

    channel_entry.grid(
        row=5,
        column=1,
        padx=18,
        pady=7,
        sticky="ew"
    )

    # --------------------------------------------------
    # MODE
    # --------------------------------------------------

    add_label(
        "Mode",
        6
    )

    mode_combo = ttk.Combobox(
        editor,
        textvariable=mode_var,
        values=[
            "momentary",
            "toggle"
        ],
        state="readonly"
    )

    mode_combo.grid(
        row=6,
        column=1,
        padx=18,
        pady=7,
        sticky="ew"
    )

    # --------------------------------------------------
    # ON VALUE
    # --------------------------------------------------

    add_label(
        "On Value",
        7
    )

    on_value_entry = tk.Entry(
        editor,
        textvariable=on_value_var,
        bg=PANEL,
        fg=TEXT,
        insertbackground=TEXT,
        relief="flat"
    )

    on_value_entry.grid(
        row=7,
        column=1,
        padx=18,
        pady=7,
        sticky="ew"
    )

    # --------------------------------------------------
    # OFF VALUE
    # --------------------------------------------------

    add_label(
        "Off Value",
        8
    )

    off_value_entry = tk.Entry(
        editor,
        textvariable=off_value_var,
        bg=PANEL,
        fg=TEXT,
        insertbackground=TEXT,
        relief="flat"
    )

    off_value_entry.grid(
        row=8,
        column=1,
        padx=18,
        pady=7,
        sticky="ew"
    )

    # --------------------------------------------------
    # METADATA
    # --------------------------------------------------

    metadata_check = tk.Checkbutton(
        editor,
        text="Clear existing Pad Labels / DSP Parameters",
        variable=clear_metadata_var,
        bg=BG,
        fg=TEXT,
        activebackground=BG,
        activeforeground=TEXT,
        selectcolor=PANEL
    )

    metadata_check.grid(
        row=9,
        column=0,
        columnspan=2,
        padx=18,
        pady=(12, 5),
        sticky="w"
    )

    # --------------------------------------------------
    # PREVIEW
    # --------------------------------------------------

    preview_var = tk.StringVar(
        value=""
    )

    preview_label = tk.Label(
        editor,
        textvariable=preview_var,
        bg=PANEL,
        fg=SUBTEXT,
        justify="left",
        anchor="nw",
        padx=10,
        pady=8,
        height=5
    )

    preview_label.grid(
        row=10,
        column=0,
        columnspan=2,
        padx=18,
        pady=10,
        sticky="ew"
    )

    def update_preview(*args):

        target = target_var.get()

        if target == "Entire Board":

            keys = []

            for row_keys in BATCH_ROWS.values():

                keys.extend(
                    row_keys
                )

        else:

            keys = BATCH_ROWS.get(
                target,
                []
            )

        try:

            start_number = int(
                number_var.get()
            )

        except ValueError:

            preview_var.set(
                "Enter a valid MIDI number."
            )

            return

        if number_mode_var.get() == "Sequential":

            assignments = []

            for index, key in enumerate(keys):

                assignments.append(
                    f"{key.upper()} → "
                    f"{type_var.get().upper()} "
                    f"{start_number + index}"
                )

        else:

            assignments = [
                f"{key.upper()} → "
                f"{type_var.get().upper()} "
                f"{start_number}"
                for key in keys
            ]

        preview_var.set(
            "\n".join(
                assignments[:12]
            )
            + (
                "\n..."
                if len(assignments) > 12
                else ""
            )
        )

    target_combo.bind(
        "<<ComboboxSelected>>",
        update_preview
    )

    type_combo.bind(
        "<<ComboboxSelected>>",
        update_preview
    )

    number_mode_combo.bind(
        "<<ComboboxSelected>>",
        update_preview
    )

    number_var.trace_add(
        "write",
        update_preview
    )

    update_preview()

    # --------------------------------------------------
    # APPLY
    # --------------------------------------------------

    def apply_batch():

        target = target_var.get()

        if target == "Entire Board":

            keys = []

            for row_keys in BATCH_ROWS.values():

                keys.extend(
                    row_keys
                )

        else:

            keys = BATCH_ROWS.get(
                target,
                []
            )

        try:

            start_number = int(
                number_var.get()
            )

            channel = int(
                channel_var.get()
            )

            on_value = int(
                on_value_var.get()
            )

            off_value = int(
                off_value_var.get()
            )

        except ValueError:

            messagebox.showerror(
                "Invalid Value",
                "Number, Channel, On Value and Off Value must be numbers.",
                parent=editor
            )

            return

        if not keys:

            messagebox.showerror(
                "No Keys",
                "No keys were selected.",
                parent=editor
            )

            return

        if not 0 <= start_number <= 127:

            messagebox.showerror(
                "Invalid Number",
                "MIDI number must be between 0 and 127.",
                parent=editor
            )

            return

        if type_var.get() == "pc" and start_number > 127:

            messagebox.showerror(
                "Invalid Program",
                "Program Change must be between 0 and 127.",
                parent=editor
            )

            return

        if (
            number_mode_var.get() == "Sequential"
            and start_number + len(keys) - 1 > 127
        ):

            messagebox.showerror(
                "Number Range",
                "Sequential assignments would exceed MIDI number 127.",
                parent=editor
            )

            return

        if not 1 <= channel <= 16:

            messagebox.showerror(
                "Invalid Channel",
                "MIDI channel must be between 1 and 16.",
                parent=editor
            )

            return

        if not 0 <= on_value <= 127:

            messagebox.showerror(
                "Invalid On Value",
                "On Value must be between 0 and 127.",
                parent=editor
            )

            return

        if not 0 <= off_value <= 127:

            messagebox.showerror(
                "Invalid Off Value",
                "Off Value must be between 0 and 127.",
                parent=editor
            )

            return

        for index, key in enumerate(keys):

            if number_mode_var.get() == "Sequential":

                midi_number = (
                    start_number + index
                )

            else:

                midi_number = start_number

            old_pedal = pedals.get(
                key,
                {}
            )

            new_pedal = {
                "type": type_var.get(),
                "number": midi_number,
                "channel": channel,
                "mode": mode_var.get(),
                "on_value": on_value,
                "off_value": off_value
            }

            if not clear_metadata_var.get():

                if old_pedal.get("label"):

                    new_pedal["label"] = (
                        old_pedal["label"]
                    )

                if old_pedal.get("dsp_parameter"):

                    new_pedal["dsp_parameter"] = (
                        old_pedal["dsp_parameter"]
                    )

            pedals[key] = new_pedal

        rebuild_board()

        save_pedals()

        editor.destroy()

        info_var.set(
            f"BATCH EDIT APPLIED: {target}"
        )

    # --------------------------------------------------
    # BUTTONS
    # --------------------------------------------------

    button_frame = tk.Frame(
        editor,
        bg=BG
    )

    button_frame.grid(
        row=11,
        column=0,
        columnspan=2,
        pady=12
    )

    tk.Button(
        button_frame,
        text="APPLY",
        width=14,
        command=apply_batch,
        bg="#333333",
        fg=TEXT,
        activebackground="#444444",
        activeforeground=TEXT
    ).pack(
        side="left",
        padx=5
    )

    tk.Button(
        button_frame,
        text="CANCEL",
        width=14,
        command=editor.destroy,
        bg="#333333",
        fg=TEXT,
        activebackground="#444444",
        activeforeground=TEXT
    ).pack(
        side="left",
        padx=5
    )


# --------------------------------------------------
# BOARD
# --------------------------------------------------

board = None


def rebuild_board():

    global board

    for widget in board.winfo_children():

        widget.destroy()

    pad_buttons.clear()

    layout = [
        [
            "1", "2", "3", "4", "5",
            "6", "7", "8", "9", "0"
        ],

        [
            "q", "w", "e", "r", "t",
            "y", "u", "i", "o", "p"
        ],

        [
            "a", "s", "d", "f", "g",
            "h", "j", "k", "l"
        ],

        [
            "z", "x", "c", "v",
            "b", "n", "m"
        ]
    ]

    for row_index, row in enumerate(layout):

        for col_index, key in enumerate(row):

            create_pad(
                key,
                row_index,
                col_index
            )

    create_pad(
        "space",
        4,
        2,
        colspan=6
    )


def create_pad(
    key,
    row,
    column,
    colspan=1
):

    pedal = pedals.get(
        key,
        {}
    )

    label = pedal.get(
        "label"
    )

    if label:

        display = label

    elif pedal.get(
        "dsp_parameter"
    ):

        display = pedal.get(
            "dsp_parameter"
        )

    else:

        pedal_type = pedal.get(
            "type",
            "cc"
        )

        number = pedal.get(
            "number",
            0
        )

        display = (
            f"{key.upper()}\n"
            f"{pedal_type.upper()} {number}"
        )

    button_bg = (
        PAD_ASSIGNED
        if (
            pedal.get("label")
            or pedal.get("dsp_parameter")
        )
        else PAD
    )

    button = tk.Button(
        board,
        text=display,
        width=8,
        height=3,
        bg=button_bg,
        fg=TEXT,
        activebackground=PAD_HOVER,
        activeforeground=TEXT,
        relief="raised",
        bd=2,
        font=(
            "Segoe UI",
            9,
            "bold"
        ),
        command=lambda k=key: edit_pedal(k)
    )

    button.grid(
        row=row,
        column=column,
        columnspan=colspan,
        padx=4,
        pady=4,
        sticky="nsew"
    )

    board.grid_columnconfigure(
        column,
        weight=1
    )

    board.grid_rowconfigure(
        row,
        weight=1
    )

    pad_buttons[key] = button


# --------------------------------------------------
# DEFAULT RESET
# --------------------------------------------------

def reset_to_default():

    if engine_running:

        messagebox.showinfo(
            "Engine Running",
            "Stop the engine before resetting the pedalboard."
        )

        return

    result = messagebox.askyesno(
        "Reset Pedalboard",
        "Reset all pedals to the default mapping?"
    )

    if not result:
        return

    pedals.clear()

    for key, value in DEFAULT_PEDALS.items():

        pedals[key] = value.copy()

    rebuild_board()

    save_pedals()

    info_var.set(
        "PEDALBOARD RESET TO DEFAULT."
    )


# --------------------------------------------------
# CLOSE
# --------------------------------------------------

def close_application():

    if engine_running:

        stop_engine()

    else:
        # Extra safety: make sure no keyboard hooks
        # remain active even if the engine state is OFF.
        keyboard.unhook_all()

    root.destroy()


# --------------------------------------------------
# MAIN WINDOW
# --------------------------------------------------

root = tk.Tk()

root.title(
    "MIDI BOARD"
)

root.geometry(
    "900x700"
)

root.minsize(
    750,
    600
)

root.configure(
    bg=BG
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

header = tk.Frame(
    root,
    bg=BG
)

header.pack(
    fill="x",
    padx=15,
    pady=(15, 5)
)


title = tk.Label(
    header,
    text="MIDI BOARD",
    bg=BG,
    fg=TEXT,
    font=(
        "Segoe UI",
        20,
        "bold"
    )
)

title.pack(
    side="left"
)


status = tk.Label(
    header,
    text="● ENGINE OFF",
    bg=BG,
    fg=RED,
    font=(
        "Segoe UI",
        10,
        "bold"
    )
)

status.pack(
    side="right",
    pady=7
)


# --------------------------------------------------
# MIDI PORT SELECTOR
# --------------------------------------------------

midi_frame = tk.Frame(
    root,
    bg=BG
)

midi_frame.pack(
    fill="x",
    padx=17,
    pady=(2, 4)
)


tk.Label(
    midi_frame,
    text="MIDI OUTPUT:",
    bg=BG,
    fg=TEXT,
    font=(
        "Segoe UI",
        9,
        "bold"
    )
).pack(
    side="left",
    padx=(0, 8)
)


midi_port_var = tk.StringVar()


midi_combo = ttk.Combobox(
    midi_frame,
    textvariable=midi_port_var,
    state="readonly",
    width=42
)

midi_combo.pack(
    side="left"
)

# Save the selected MIDI port whenever
# the user changes the dropdown.
midi_combo.bind(
    "<<ComboboxSelected>>",
    midi_port_selected
)


refresh_button = tk.Button(
    midi_frame,
    text="REFRESH",
    width=9,
    command=refresh_midi_ports,
    bg="#333333",
    fg=TEXT,
    activebackground="#444444",
    activeforeground=TEXT
)

refresh_button.pack(
    side="left",
    padx=6
)


midi_info = tk.Label(
    root,
    text="MIDI: Detecting...",
    bg=BG,
    fg=SUBTEXT,
    font=(
        "Segoe UI",
        9
    )
)

midi_info.pack(
    anchor="w",
    padx=17
)


# --------------------------------------------------
# INFO
# --------------------------------------------------

info_var = tk.StringVar(
    value="Click a pad to edit its MIDI / DSP assignment."
)


info_label = tk.Label(
    root,
    textvariable=info_var,
    bg=BG,
    fg=SUBTEXT,
    font=(
        "Segoe UI",
        9
    )
)

info_label.pack(
    anchor="w",
    padx=17,
    pady=(3, 10)
)


# --------------------------------------------------
# BOARD
# --------------------------------------------------

board = tk.Frame(
    root,
    bg=BG
)

board.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=5
)

rebuild_board()


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

footer = tk.Frame(
    root,
    bg=PANEL
)

footer.pack(
    fill="x",
    padx=10,
    pady=10,
    ipady=8
)


keyboard_lock_button = tk.Button(
    footer,
    text="🔒 KEYBOARD LOCK ON",
    width=20,
    command=toggle_keyboard_lock,
    bg=GREEN,
    fg=BG,
    activebackground=GREEN,
    activeforeground=BG
)

keyboard_lock_button.pack(
    side="left",
    padx=3
)


keyboard_lock_status = tk.Label(
    footer,
    text="● LOCKED",
    bg=PANEL,
    fg=GREEN,
    font=(
        "Segoe UI",
        9,
        "bold"
    )
)

keyboard_lock_status.pack(
    side="left",
    padx=(5, 12)
)


engine_button = tk.Button(
    footer,
    text="○ ENGINE OFF",
    width=15,
    command=toggle_engine,
    bg="#333333",
    fg=TEXT,
    activebackground="#444444",
    activeforeground=TEXT
)

engine_button.pack(
    side="left",
    padx=3
)


default_button = tk.Button(
    footer,
    text="DEFAULT",
    width=12,
    command=reset_to_default,
    bg="#333333",
    fg=TEXT,
    activebackground="#444444",
    activeforeground=TEXT
)

default_button.pack(
    side="left",
    padx=3
)


batch_button = tk.Button(
    footer,
    text="BATCH EDIT",
    width=12,
    command=batch_edit,
    bg="#333333",
    fg=TEXT,
    activebackground="#444444",
    activeforeground=TEXT
)

batch_button.pack(
    side="left",
    padx=3
)


save_button = tk.Button(
    footer,
    text="SAVE",
    width=12,
    command=save_pedals,
    bg="#333333",
    fg=TEXT,
    activebackground="#444444",
    activeforeground=TEXT
)

save_button.pack(
    side="left",
    padx=3
)


close_button = tk.Button(
    footer,
    text="CLOSE",
    width=12,
    command=close_application,
    bg="#333333",
    fg=TEXT,
    activebackground="#444444",
    activeforeground=TEXT
)

close_button.pack(
    side="right",
    padx=3
)


# --------------------------------------------------
# INITIAL MIDI PORT SCAN
# --------------------------------------------------

refresh_midi_ports()

update_status()
update_keyboard_lock_ui()


root.protocol(
    "WM_DELETE_WINDOW",
    close_application
)


root.mainloop()