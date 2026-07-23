from datetime import timedelta


def format_size(num):

    if num is None:
        return "--"

    units = ["B", "KB", "MB", "GB", "TB", "PB"]

    value = float(num)

    for unit in units:

        if value < 1024 or unit == units[-1]:

            if unit == "B":
                return f"{int(value)} {unit}"

            return f"{value:.2f} {unit}"

        value /= 1024


def format_speed(num):

    if num is None:
        return "--"

    return f"{format_size(num)}/s"


def format_eta(seconds):

    if seconds is None:
        return "--"

    try:
        seconds = int(seconds)
    except:
        return "--"

    if seconds < 0:
        return "--"

    if seconds < 60:
        return f"{seconds}s"

    if seconds < 3600:

        m, s = divmod(seconds, 60)

        return f"{m}m {s}s"

    if seconds < 86400:

        h, rem = divmod(seconds, 3600)

        m = rem // 60

        return f"{h}h {m}m"

    d = timedelta(seconds=seconds)

    days = d.days

    hours = d.seconds // 3600

    return f"{days}d {hours}h"


def format_storage(used, total):

    free = max(total - used, 0)

    return (
        f"{format_size(free)} free\n"
        f"of {format_size(total)}"
    )


def format_percentage(value):

    try:
        return f"{float(value):.1f}%"
    except:
        return "--"


def shorten_filename(name, length=42):

    if not name:
        return "Unknown"

    if len(name) <= length:
        return name

    left = length // 2 - 2
    right = length // 2 - 3

    return f"{name[:left]}...{name[-right:]}"


def average(values):

    if not values:
        return 0

    return sum(values) / len(values)