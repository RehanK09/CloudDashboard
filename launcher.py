import json
import subprocess
import os
import time

BASE = os.path.dirname(__file__)

with open(os.path.join(BASE, "config.json"), "r") as f:
    cfg = json.load(f)

rclone = cfg["rclone"]
remote = cfg["remote"]
drive = cfg["drive"]
port = cfg["rc_port"]

cmd = [
    rclone,
    "mount",
    remote,
    drive,
    "--rc",
    "--rc-no-auth",
    "--rc-addr",
    f"127.0.0.1:{port}",
    "--vfs-cache-mode",
    "full",
    "--buffer-size",
    "64M",
    "--stats",
    "1s"
]

mount = subprocess.Popen(
    cmd,
    creationflags=subprocess.CREATE_NO_WINDOW
)

time.sleep(3)

subprocess.call(["python", "dashboard.py"])

mount.terminate()