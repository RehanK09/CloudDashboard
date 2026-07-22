import customtkinter as ctk
import requests
import os
import subprocess
from tkinter import messagebox

from history import HistoryWindow
from settings import SettingsWindow
from storage import get_storage_strings
from utils import (
    ask_exit,
    shutdown_everything,
    open_drive,
    format_speed,
    format_size
)
from graph import SpeedGraph
from logger import CloudLogger

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

RC_PORT = 5572
DRIVE_LETTER = "X:"

graph = SpeedGraph()

CloudLogger.dashboard_opened()

app = ctk.CTk()
app.title("Cloud Dashboard v2")
app.geometry("1050x720")
app.minsize(1000, 680)

running_transfer = False


# ---------------------------
# HEADER
# ---------------------------

header = ctk.CTkFrame(app, height=60)
header.pack(fill="x", padx=10, pady=10)

title = ctk.CTkLabel(
    header,
    text="☁ Cloud Dashboard",
    font=("Segoe UI", 26, "bold")
)

title.pack(side="left", padx=20)

history_btn = ctk.CTkButton(
    header,
    text="History",
    width=110,
    command=lambda: HistoryWindow(app)
)

history_btn.pack(side="right", padx=8)

settings_btn = ctk.CTkButton(
    header,
    text="Settings",
    width=110,
    command=lambda: SettingsWindow(app)
)

settings_btn.pack(side="right", padx=8)

drive_btn = ctk.CTkButton(
    header,
    text="Open Drive",
    width=110,
    command=lambda: open_drive(DRIVE_LETTER)
)

drive_btn.pack(side="right", padx=8)


# ---------------------------
# STATUS CARD
# ---------------------------

status_card = ctk.CTkFrame(app)

status_card.pack(fill="x", padx=10)

status = ctk.CTkLabel(
    status_card,
    text="Connecting...",
    font=("Segoe UI",20,"bold")
)

status.pack(anchor="w", padx=20, pady=(12,4))

speed = ctk.CTkLabel(status_card,text="Speed : --")
speed.pack(anchor="w", padx=20)

uploaded = ctk.CTkLabel(status_card,text="Uploaded : --")
uploaded.pack(anchor="w", padx=20)

transfers = ctk.CTkLabel(status_card,text="Transfers : --")
transfers.pack(anchor="w", padx=20)

errors = ctk.CTkLabel(status_card,text="Errors : --")
errors.pack(anchor="w", padx=20, pady=(0,12))


# ---------------------------
# PROGRESS AREA
# ---------------------------

progress_frame = ctk.CTkFrame(app)
progress_frame.pack(fill="x", padx=10, pady=10)

storage_label = ctk.CTkLabel(
    progress_frame,
    text="Cloud Storage"
)
storage_label.pack(anchor="w", padx=20)

storage_bar = ctk.CTkProgressBar(progress_frame)
storage_bar.pack(fill="x", padx=20)
storage_bar.set(0)

storage_info = ctk.CTkLabel(progress_frame,text="--")
storage_info.pack(anchor="w", padx=20, pady=(0,12))

upload_label = ctk.CTkLabel(
    progress_frame,
    text="Current Upload"
)
upload_label.pack(anchor="w", padx=20)

upload_bar = ctk.CTkProgressBar(progress_frame)
upload_bar.pack(fill="x", padx=20)
upload_bar.set(0)

upload_info = ctk.CTkLabel(progress_frame,text="Idle")
upload_info.pack(anchor="w", padx=20,pady=(0,12))

queue_label = ctk.CTkLabel(
    progress_frame,
    text="Upload Queue"
)
queue_label.pack(anchor="w", padx=20)

queue_bar = ctk.CTkProgressBar(progress_frame)
queue_bar.pack(fill="x", padx=20)
queue_bar.set(0)

queue_info = ctk.CTkLabel(progress_frame,text="0 Files")
queue_info.pack(anchor="w", padx=20,pady=(0,12))

today_label = ctk.CTkLabel(
    progress_frame,
    text="Today's Upload"
)
today_label.pack(anchor="w", padx=20)

today_bar = ctk.CTkProgressBar(progress_frame)
today_bar.pack(fill="x", padx=20)
today_bar.set(0)

today_info = ctk.CTkLabel(progress_frame,text="0 GB")
today_info.pack(anchor="w", padx=20,pady=(0,15))


# ---------------------------
# RECENT ACTIVITY
# ---------------------------

activity_frame = ctk.CTkFrame(app)

activity_frame.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)

activity_title = ctk.CTkLabel(
    activity_frame,
    text="Recent Activity",
    font=("Segoe UI",18,"bold")
)

activity_title.pack(anchor="w", padx=15, pady=10)

activity_box = ctk.CTkTextbox(
    activity_frame,
    height=180
)

activity_box.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=(0,15)
)

# ---------------------------
# LOAD RECENT HISTORY
# ---------------------------

def load_recent_activity():

    activity_box.delete("1.0", "end")

    try:

        from history import load_history

        items = load_history()[:15]

        if not items:

            activity_box.insert(
                "end",
                "\nNo upload history yet."
            )

            return

        for item in items:

            icon = "✔"

            if item.get("status", "") != "SUCCESS":
                icon = "❌"

            activity_box.insert(
                "end",
                f"{icon} {item.get('filename','Unknown')}    "
                f"{item.get('size','')}    "
                f"{item.get('status','')}\n"
            )

    except Exception as e:

        activity_box.insert(
            "end",
            str(e)
        )


# ---------------------------
# UPDATE DASHBOARD
# ---------------------------

def update_dashboard():

    global running_transfer

    try:

        r = requests.post(
            f"http://127.0.0.1:{RC_PORT}/core/stats",
            timeout=2
        )

        data = r.json()

        status.configure(
            text="🟢 Connected"
        )

        current_speed = data.get(
            "speed",
            0
        )

        graph.add(current_speed)

        speed.configure(

            text=f"Speed : {format_speed(current_speed)}"

        )

        uploaded.configure(

            text=f"Uploaded : {format_size(data.get('bytes',0))}"

        )

        transfers_count = data.get(
            "transferring",
            0
        )

        transfers.configure(

            text=f"Transfers : {transfers_count}"

        )

        errors.configure(

            text=f"Errors : {data.get('errors',0)}"

        )

        running_transfer = transfers_count > 0

        storage = get_storage_strings()

        storage_bar.set(
            storage["percent"] / 100
        )

        storage_info.configure(

            text=f'{storage["used"]} / {storage["total"]}    ({storage["percent"]:.1f}%)'

        )

        if running_transfer:

            upload_bar.set(0.5)

            upload_info.configure(

                text="Uploading..."

            )

        else:

            upload_bar.set(0)

            upload_info.configure(

                text="Idle"

            )

        queue_bar.set(
            min(
                transfers_count / 10,
                1
            )
        )

        queue_info.configure(

            text=f"{transfers_count} Active"

        )

        goal = 50 * 1024 * 1024 * 1024

        uploaded_today = data.get(
            "bytes",
            0
        )

        today_percent = min(
            uploaded_today / goal,
            1
        )

        today_bar.set(today_percent)

        today_info.configure(

            text=f"{format_size(uploaded_today)}"

        )

        load_recent_activity()

    except Exception:

        running_transfer = False

        status.configure(

            text="🔴 Waiting for rclone..."

        )

        speed.configure(

            text="Speed : --"

        )

        uploaded.configure(

            text="Uploaded : --"

        )

        transfers.configure(

            text="Transfers : --"

        )

        errors.configure(

            text="Errors : --"

        )

        storage_bar.set(0)

        upload_bar.set(0)

        queue_bar.set(0)

        today_bar.set(0)

    app.after(
        1000,
        update_dashboard
    )

# ---------------------------
# CONTROL BUTTONS
# ---------------------------

controls = ctk.CTkFrame(app)
controls.pack(fill="x", padx=10, pady=(0,10))

pause_btn = ctk.CTkButton(
    controls,
    text="Pause",
    width=120
)

pause_btn.pack(side="left", padx=8, pady=10)

resume_btn = ctk.CTkButton(
    controls,
    text="Resume",
    width=120
)

resume_btn.pack(side="left", padx=8)

stop_btn = ctk.CTkButton(
    controls,
    text="Stop",
    width=120,
    fg_color="#c62828",
    hover_color="#8e0000"
)

stop_btn.pack(side="left", padx=8)

refresh_btn = ctk.CTkButton(
    controls,
    text="Refresh",
    width=120,
    command=load_recent_activity
)

refresh_btn.pack(side="right", padx=8)


# ---------------------------
# LIVE SPEED GRAPH
# ---------------------------

graph_frame = ctk.CTkFrame(app)
graph_frame.pack(fill="x", padx=10, pady=(0,10))

graph_title = ctk.CTkLabel(
    graph_frame,
    text="Live Upload Speed",
    font=("Segoe UI",16,"bold")
)

graph_title.pack(anchor="w", padx=15, pady=(10,0))

graph_canvas = ctk.CTkCanvas(
    graph_frame,
    height=130,
    bg="#202020",
    highlightthickness=0
)

graph_canvas.pack(fill="x", padx=15, pady=10)


def draw_graph():

    graph_canvas.delete("all")

    values = graph.percent()

    if len(values) < 2:

        return

    w = graph_canvas.winfo_width()

    h = graph_canvas.winfo_height()

    if w <= 5:
        app.after(500, draw_graph)
        return

    step = w / (len(values)-1)

    pts = []

    for i,v in enumerate(values):

        x = i * step

        y = h - ((v/100) * h)

        pts.extend((x,y))

    try:

        graph_canvas.create_line(
            *pts,
            width=2,
            smooth=True,
            fill="#00d4ff"
        )

    except:
        pass

    app.after(
        1000,
        draw_graph
    )


# ---------------------------
# SAFE EXIT
# ---------------------------

def close_dashboard():

    global running_transfer

    if not ask_exit(running_transfer):

        return

    CloudLogger.dashboard_closed()

    shutdown_everything(DRIVE_LETTER)

    app.destroy()


app.protocol(
    "WM_DELETE_WINDOW",
    close_dashboard
)


# ---------------------------
# START
# ---------------------------

load_recent_activity()

draw_graph()

update_dashboard()

app.mainloop()



# ---------------------------
# RCLONE RC COMMANDS
# ---------------------------

def rc_call(command, payload=None):

    try:

        if payload is None:
            payload = {}

        requests.post(
            f"http://127.0.0.1:{RC_PORT}/{command}",
            json=payload,
            timeout=2
        )

        return True

    except:

        return False


def pause_uploads():

    rc_call(
        "core/bwlimit",
        {
            "rate": "1b"
        }
    )

    CloudLogger.info(
        "Uploads Paused"
    )


def resume_uploads():

    rc_call(
        "core/bwlimit",
        {
            "rate": "off"
        }
    )

    CloudLogger.info(
        "Uploads Resumed"
    )


def stop_uploads():

    try:

        requests.post(

            f"http://127.0.0.1:{RC_PORT}/job/stop",

            json={
                "jobid": -1
            },

            timeout=2

        )

    except:
        pass

    CloudLogger.warning(
        "All Uploads Stopped"
    )


pause_btn.configure(
    command=pause_uploads
)

resume_btn.configure(
    command=resume_uploads
)

stop_btn.configure(
    command=stop_uploads
)


# ---------------------------
# HISTORY AUTO LOGGER
# ---------------------------

_last_uploaded = 0


def watch_uploads():

    global _last_uploaded

    try:

        r = requests.post(
            f"http://127.0.0.1:{RC_PORT}/core/stats",
            timeout=2
        )

        d = r.json()

        uploaded_now = d.get(
            "bytes",
            0
        )

        if uploaded_now > _last_uploaded:

            difference = uploaded_now - _last_uploaded

            try:

                from history import add_history

                add_history(

                    filename="Unknown File",

                    size=format_size(
                        difference
                    ),

                    status="SUCCESS",

                    destination=DRIVE_LETTER,

                    speed=format_speed(
                        d.get(
                            "speed",
                            0
                        )
                    )

                )

            except:
                pass

            _last_uploaded = uploaded_now

    except:
        pass

    app.after(
        5000,
        watch_uploads
    )


watch_uploads()


# ---------------------------
# STARTUP STORAGE
# ---------------------------

try:

    storage = get_storage_strings()

    storage_bar.set(
        storage["percent"]/100
    )

    storage_info.configure(

        text=f'{storage["used"]} / {storage["total"]}'

    )

except:

    pass


# ---------------------------
# WINDOW TITLE REFRESH
# ---------------------------

def update_title():

    try:

        r = requests.post(

            f"http://127.0.0.1:{RC_PORT}/core/stats",

            timeout=2

        )

        d = r.json()

        sp = format_speed(
            d.get(
                "speed",
                0
            )
        )

        tr = d.get(
            "transferring",
            0
        )

        app.title(

            f"Cloud Dashboard | {sp} | {tr} Transfer(s)"

        )

    except:

        app.title(
            "Cloud Dashboard"
        )

    app.after(
        1000,
        update_title
    )


update_title()


# ---------------------------
# READY
# ---------------------------

CloudLogger.info(
    "Dashboard Ready"
)