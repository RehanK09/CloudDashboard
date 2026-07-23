import subprocess
import requests
import time
import sys
import os

BASE = os.path.dirname(os.path.abspath(__file__))

BAT = os.path.join(BASE, "MountCloud.bat")

PORT = 5572


def rc_ready():

    try:

        requests.post(
            f"http://127.0.0.1:{PORT}/core/stats",
            timeout=1
        )

        return True

    except:

        return False


def kill_rclone():

    subprocess.call(

        [
            "taskkill",
            "/F",
            "/IM",
            "rclone.exe"
        ],

        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


def main():

    kill_rclone()

    rclone = subprocess.Popen(

        BAT,

        cwd=BASE,

        creationflags=subprocess.CREATE_NEW_CONSOLE

    )

    print("Waiting for rclone...")

    while not rc_ready():

        time.sleep(1)

    print("Connected")




    dashboard = subprocess.Popen(

        [sys.executable, "app_v4.py"],

        cwd=BASE

    )


    dashboard.wait()

    kill_rclone()

    try:
        rclone.kill()
    except:
        pass


if __name__ == "__main__":

    main()