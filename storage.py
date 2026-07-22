import json
import requests

with open("config.json", "r", encoding="utf-8") as f:
    CONFIG = json.load(f)

PORT = CONFIG["rc_port"]
REMOTE = CONFIG["remote"]


def human_size(size):

    size = float(size)

    units = ["B","KB","MB","GB","TB","PB"]

    for u in units:

        if size < 1024:
            return f"{size:.2f} {u}"

        size /= 1024

    return f"{size:.2f} EB"


def get_storage():

    try:

        r = requests.post(

            f"http://127.0.0.1:{PORT}/operations/about",

            json={

                "fs": REMOTE

            },

            timeout=3

        )

        return r.json()

    except:

        return None


def get_storage_strings():

    data = get_storage()

    if not data:

        return {

            "used":"0 B",
            "total":"0 B",
            "free":"0 B",
            "percent":0

        }

    used = data.get("used",0)
    total = data.get("total",0)
    free = data.get("free",0)

    percent = 0

    if total:

        percent = used / total * 100

    return {

        "used":human_size(used),
        "total":human_size(total),
        "free":human_size(free),
        "percent":percent

    }