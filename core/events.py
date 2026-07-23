"""
core/events.py
--------------
Tiny synchronous pub/sub event bus.

This is what lets every widget (header, drive cards, transfer cards,
graph, stats tiles, activity list) react to new data WITHOUT each one
running its own poll timer or importing core/api.py directly.

core/refresh.py is the ONLY thing that reads from core/api.py. It
publishes events here on a Tkinter after() tick; widgets just
subscribe. That keeps the "one poller, one source of truth" rule from
api.py intact even as the UI splits into a dozen widget files.

Not thread-aware on purpose: publish() must only ever be called from
the Tkinter thread (i.e. from inside refresh.py's after() tick), never
from api.py's background polling thread. That's what makes it safe
for subscriber callbacks to touch widgets directly.
"""

from collections import defaultdict

# Event name constants so widgets don't hardcode typo-prone strings.
STATS_UPDATED = "stats_updated"              # payload: rclone_api.get_stats() dict
STORAGE_UPDATED = "storage_updated"          # payload: rclone_api.get_storage() dict
CONNECTION_CHANGED = "connection_changed"    # payload: bool (True = online)
PAUSE_STATE_CHANGED = "pause_state_changed"  # payload: bool (True = paused)
# ^ rclone/api.py has no concept of "paused" (pausing is done via a
#   core/bwlimit throttle, not a real backend state) — this event is
#   published by widgets/toolbar.py when Start/Pause is clicked, so
#   status_badge.py can show PAUSED without api.py needing to change.
HISTORY_UPDATED = "history_updated"          # payload: one history.json entry (dict)
# ^ published by history.py's HistoryTracker the moment it writes a
#   finished transfer to history.json, so widgets/activity.py can show
#   it instantly instead of re-reading the file on a timer.


class EventBus:
    def __init__(self):
        self._subscribers = defaultdict(list)

    def subscribe(self, event_name, callback):
        """Register callback(data) to run when event_name fires.
        Returns an unsubscribe function — widgets should call it in
        their own destroy/cleanup so a closed window doesn't keep
        getting called with stale references."""
        self._subscribers[event_name].append(callback)

        def _unsubscribe():
            try:
                self._subscribers[event_name].remove(callback)
            except ValueError:
                pass
        return _unsubscribe

    def publish(self, event_name, data=None):
        for callback in list(self._subscribers[event_name]):
            try:
                callback(data)
            except Exception as e:
                # One broken widget callback should never take down the
                # refresh loop or every other widget listening in.
                print(f"[events] subscriber for '{event_name}' raised: {e}")


# Shared bus — import this, don't instantiate your own EventBus().
bus = EventBus()
