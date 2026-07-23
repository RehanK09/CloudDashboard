"""
api.py
------
Centralized, thread-safe client for rclone's Remote Control (RC) API.

WHY THIS FILE EXISTS
This is the fix for the dashboard's core architectural problem: dashboard.py
currently has FIVE separate blocking `requests.post(...)` calls, each on its
own `app.after(1000, ...)` timer, running directly on the Tkinter main thread
(update_dashboard, draw_graph indirectly via update_dashboard, watch_uploads,
update_title, plus get_storage_strings on every tick). Every one of those
hits the network and blocks the GUI thread while it waits — that's the
freeze. It's also 4-5x more RC calls than needed, and none of them read
config.json, so remote/port are hardcoded in three different places.

RcloneAPI runs ONE background thread. It polls /core/stats every 1s and
/operations/about every 30s, and stores the results behind a lock. Every
other module reads from this cache with a plain dict copy — no network
call, no blocking, ever, on the Tkinter thread.

It also uses the REAL per-file data rclone already gives us in
/core/stats -> "transferring": actual filename, actual bytes/size,
actual percentage, actual speed, actual eta. That's what fixes
"History is fake" / "Unknown File" and the fake 0.5 upload bar in
dashboard.py's update_dashboard().
"""

import json
import queue
import threading
import time

import requests


class RcloneAPI:

    STATS_INTERVAL_ACTIVE = 0.10 # "Stats every 1 sec" (from your goals)
    STATS_INTERVAL_IDLE = 0.50   # "Storage every 30 sec"
    STORAGE_INTERVAL = 5

    def __init__(self, config_path="config.json"):
        self._config_path = config_path
        self._config = self._load_config()

        drive = self._config["drives"][0]

        self.rclone_path = drive["rclone"]
        self.remote = drive["remote"]
        self.drive = drive["drive"]
        self.rc_port = self._config.get("rc_port", 5572)
        self.base_url = f"http://127.0.0.1:{self.rc_port}"

        self._session = requests.Session()
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread = None

        self._stats = {
            "connected": False,
            "speed": 0,
            "bytes": 0,
            "errors": 0,
            "transferring": [],
            "last_error": None,
            "updated": time.time(),
            "download_speed":0,
            "download_bytes":0,
        }
        self._storage = {
            "used": 0,
            "total": 0,
            "free": 0,
            "percent": 0.0,
            "fetched_at": 0.0,
        }

        # Optional event queue: instead of dashboard.py polling get_stats()
        # on its own timer, it can call poll_events() each tick to drain
        # only what's new. Still Tkinter-safe — nothing is pushed onto the
        # GUI thread, this is just a queue the GUI reads from.
        self._events = queue.Queue()

    # ----------------------------------------------------------------
    # config
    # ----------------------------------------------------------------
    def _load_config(self):
        try:
            with open(self._config_path, "r") as f:
                return json.load(f)
        except Exception:
            return {}

    def reload_config(self):
        """Call after Settings saves config.json so new values take effect
        without restarting the dashboard."""
        with self._lock:
            self._config = self._load_config()
        drive = self._config["drives"][0]

        self.rclone_path = drive["rclone"]
        self.remote = drive["remote"]
        self.drive = drive["drive"]
        self.rc_port = self._config.get("rc_port", self.rc_port)
    # ----------------------------------------------------------------
    # lifecycle
    # ----------------------------------------------------------------
    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._poll_loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop_event.set()

    # ----------------------------------------------------------------
    # background loop — this thread NEVER touches Tkinter widgets
    # ----------------------------------------------------------------

    def _poll_loop(self):

        last_storage_fetch = 0.0

        while not self._stop_event.is_set():

            self._poll_stats()

            now = time.time()

            if now - last_storage_fetch >= self.STORAGE_INTERVAL:

                self._poll_storage()

                last_storage_fetch = now

            stats = self.get_stats()

            if stats.get("transferring"):

                interval = self.STATS_INTERVAL_ACTIVE

            else:

                interval = self.STATS_INTERVAL_IDLE

            self._stop_event.wait(interval)








    def _poll_stats(self):
        try:
            r = self._session.post(f"{self.base_url}/core/stats", timeout=2)
            r.raise_for_status()
            data = r.json()

            transferring = []
            for item in data.get("transferring", []) or []:
                size = item.get("size", 0) or 0
                bytes_done = item.get("bytes", 0) or 0
                pct = item.get("percentage")
                if pct is None:
                    pct = (bytes_done / size * 100) if size else 0
                transferring.append({
                    "name": item.get("name", "Unknown"),
                    "size": size,
                    "bytes": bytes_done,
                    "percentage": pct,
                    "speed": item.get("speed", 0) or 0,
                    "eta": item.get("eta"),
                })

            with self._lock:
                self._stats = {
                    "connected": True,
                    "speed": data.get("speed", 0) or 0,
                    "bytes": data.get("bytes", 0) or 0,
                    "errors": data.get("errors", 0) or 0,
                    "transferring": transferring,
                    "last_error": None,
                }
                snapshot = dict(self._stats)
            self._events.put(("stats", snapshot))
        except Exception as e:
            with self._lock:
                self._stats["connected"] = False
                self._stats["transferring"] = []
                self._stats["last_error"] = str(e)
                snapshot = dict(self._stats)
            self._events.put(("stats", snapshot))

    def _poll_storage(self):
        # NOTE re: your review question #1 — checked rclone's rc docs:
        # `fs` wants the remote name with its trailing colon and no path
        # for the root (e.g. "drive:"), which is exactly how config.json
        # stores it ("GAurGhusMAurMhus:"). Nothing to strip here.
        try:
            r = self._session.post(
                f"{self.base_url}/operations/about",
                json={"fs": self.remote},
                timeout=5,
            )
            r.raise_for_status()
            data = r.json()
            total = data.get("total", 0) or 0
            used = data.get("used", 0) or 0
            free = data.get("free", max(total - used, 0))
            percent = (used / total * 100) if total else 0.0

            with self._lock:
                self._storage = {
                    "used": used,
                    "total": total,
                    "free": free,
                    "percent": percent,
                    "fetched_at": time.time(),
                }
                snapshot = dict(self._storage)
            self._events.put(("storage", snapshot))
        except Exception:
            # Keep the last known-good storage numbers rather than
            # flashing the UI to zero every time this call is slow.
            pass

    # ----------------------------------------------------------------
    # thread-safe reads — call these from the Tkinter thread freely
    # ----------------------------------------------------------------
    def get_stats(self):
        with self._lock:
            return dict(self._stats)

    def get_storage(self):
        with self._lock:
            return dict(self._storage)

    def is_connected(self):
        with self._lock:
            return self._stats["connected"]

    def get_current_transfer(self):
        """Returns the single largest active transfer, or None if idle.
        This is the REAL replacement for the fake upload_bar.set(0.5)."""
        with self._lock:
            items = self._stats["transferring"]
        if not items:
            return None
        return max(items, key=lambda t: t.get("bytes", 0))

    def poll_events(self, max_items=10):
        """Drain up to max_items pending ("stats"|"storage", snapshot)
        events. Call this from a cheap app.after(200, ...) loop instead of
        re-reading get_stats()/get_storage() on a timer — same effect,
        but the dashboard only does work when something actually changed."""
        events = []
        for _ in range(max_items):
            try:
                events.append(self._events.get_nowait())
            except queue.Empty:
                break
        return events

    # ----------------------------------------------------------------
    # fire-and-forget controls — these also never block the GUI thread
    # ----------------------------------------------------------------
    def pause_uploads(self):
        self._async_call("core/bwlimit", {"rate": "1b"})

    def resume_uploads(self):
        self._async_call("core/bwlimit", {"rate": "off"})

    def stop_all(self):
        # Re: review question #2 — jobid=-1 is not a real rclone jobid,
        # this would 400 with "job not found". There's no "stop everything"
        # endpoint, so instead we list the real running jobids and stop
        # each one individually.
        #
        # Caveat worth knowing: rclone's job/stop cancels the job's
        # context, but a file that's already mid-transfer inside that job
        # can finish that single file before the cancellation takes
        # effect (this is an upstream rclone behavior, not something we
        # can fix client-side). Treat this as "stop the queue", not an
        # instant kill of whatever is transferring right now.
        def _run():
            try:
                r = self._session.post(f"{self.base_url}/job/list", timeout=3)
                r.raise_for_status()
                jobids = r.json().get("jobids", []) or []
            except Exception:
                jobids = []
            for jid in jobids:
                try:
                    self._session.post(
                        f"{self.base_url}/job/stop",
                        json={"jobid": jid},
                        timeout=3,
                    )
                except Exception:
                    pass
        threading.Thread(target=_run, daemon=True).start()

    def _async_call(self, endpoint, payload):
        def _run():
            try:
                self._session.post(f"{self.base_url}/{endpoint}", json=payload, timeout=3)
            except Exception:
                pass
        threading.Thread(target=_run, daemon=True).start()


# Every module (dashboard, history, storage, graph) should import THIS
# shared instance instead of creating its own RcloneAPI() or calling
# requests directly. One poller, one source of truth.
rclone_api = RcloneAPI()
