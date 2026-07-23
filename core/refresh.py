"""
core/refresh.py
----------------
Adaptive refresh scheduler for the v4 dashboard.

This is the ONLY thing in the entire v4 UI that reads from
core/api.py. It runs on a plain Tkinter after() timer — never a
background thread, because reading rclone_api's already-cached dict
is instant, there's nothing to gain from a thread here. It republishes
whatever it reads through core/events.py; every widget subscribes
instead of polling on its own.

Adaptive rate, per the v4 spec:
- 100ms tick while something is transferring
- 500ms tick while idle
- storage is re-published every 5s regardless of tick rate

One thing worth being explicit about: core/api.py itself only
re-fetches storage from rclone every 30s internally (that's the
backend behavior — untouched, per your "don't rewrite the API" rule).
This scheduler's "every 5s" is just how often the UI re-announces
whatever number is already cached; it does not add new network calls,
and the number itself still only changes at api.py's own 30s pace.

Connection state (feeds the ONLINE/OFFLINE/UPLOADING pill) is checked
on every single tick, so it's accurate within one tick — effectively
instant at both 100ms and 500ms.
"""

from core.api import rclone_api
from core.events import bus, STATS_UPDATED, STORAGE_UPDATED, CONNECTION_CHANGED

IDLE_INTERVAL_MS = 500
ACTIVE_INTERVAL_MS = 100
STORAGE_INTERVAL_MS = 5000


class RefreshScheduler:
    def __init__(self, root):
        self._root = root
        self._running = False
        self._last_connected = None
        self._ms_since_storage = STORAGE_INTERVAL_MS  # publish once immediately
        self._current_interval = IDLE_INTERVAL_MS

    def start(self):
        if self._running:
            return
        self._running = True
        self._tick()

    def stop(self):
        self._running = False

    def _tick(self):
        if not self._running:
            return

        stats = rclone_api.get_stats()
        bus.publish(STATS_UPDATED, stats)

        connected = stats["connected"]
        if connected != self._last_connected:
            self._last_connected = connected
            bus.publish(CONNECTION_CHANGED, connected)

        self._ms_since_storage += self._current_interval
        if self._ms_since_storage >= STORAGE_INTERVAL_MS:
            self._ms_since_storage = 0
            bus.publish(STORAGE_UPDATED, rclone_api.get_storage())

        is_uploading = bool(stats["transferring"])
        self._current_interval = ACTIVE_INTERVAL_MS if is_uploading else IDLE_INTERVAL_MS

        self._root.after(self._current_interval, self._tick)


_scheduler = None


def start_refresh(root):
    """Call once from app_v4.py / dashboard_v4.py after the root window
    exists. Safe to call more than once — reuses the same scheduler."""
    global _scheduler
    if _scheduler is None:
        _scheduler = RefreshScheduler(root)
    _scheduler.start()
    return _scheduler
