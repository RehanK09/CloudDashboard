import os
import subprocess
import platform
from tkinter import messagebox


def open_drive(letter="X:"):

    try:
        os.startfile(letter)
    except Exception:
        pass


def kill_rclone():

    try:

        if platform.system() == "Windows":

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

        else:

            subprocess.call(
                [
                    "pkill",
                    "-f",
                    "rclone"
                ]
            )

    except Exception:
        pass


def unmount_drive(letter="X:"):

    try:

        subprocess.call(
            [
                "mountvol",
                letter,
                "/D"
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    except Exception:
        pass


def shutdown_everything(letter="X:"):

    kill_rclone()

    unmount_drive(letter)


def ask_exit(upload_running=False):

    if upload_running:

        return messagebox.askyesno(

            "Upload Running",

            "An upload is currently running.\n\n"
            "Closing will stop all uploads.\n\n"
            "Do you want to exit?"

        )

    return messagebox.askyesno(

        "Exit",

        "Close Cloud Dashboard?"

    )