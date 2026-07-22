import customtkinter as ctk
import requests

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()

app.title("Cloud Dashboard")
app.geometry("520x350")

status = ctk.CTkLabel(app, text="Status : Connecting...", font=("Segoe UI",18))
status.pack(pady=10)

speed = ctk.CTkLabel(app, text="")
speed.pack()

uploaded = ctk.CTkLabel(app, text="")
uploaded.pack()

transfers = ctk.CTkLabel(app, text="")
transfers.pack()

PORT = 5572


def update():

    try:

        r = requests.post(f"http://127.0.0.1:{PORT}/core/stats")

        data = r.json()

        status.configure(text="🟢 Connected")

        speed.configure(
            text=f"Speed : {data.get('speed',0)/1024/1024:.2f} MB/s"
        )

        uploaded.configure(
            text=f"Uploaded : {data.get('bytes',0)/1024/1024:.2f} MB"
        )

        transfers.configure(
            text=f"Transfers : {data.get('transferring',0)}"
        )

    except Exception:

        status.configure(text="🔴 Waiting for rclone...")

    app.after(1000, update)

update()

app.mainloop()