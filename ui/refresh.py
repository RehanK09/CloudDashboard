import time

from api import rclone_api
from history import history_tracker


class RefreshManager:

    def __init__(
        self,
        app,
        status_card,
        progress_card,
        activity_card,
        graph_card,
        graph
    ):

        self.app = app

        self.status_card = status_card
        self.progress_card = progress_card
        self.activity_card = activity_card
        self.graph_card = graph_card
        self.graph = graph

        self.last_activity_refresh = 0

    def start(self):

        rclone_api.start()

        self.activity_card.refresh()

        self.update()

    def stop(self):

        rclone_api.stop()

    def force_refresh(self):

        self.activity_card.refresh()

        self.update_once()

    def update(self):

        self.update_once()

        self.app.after(
            250,
            self.update
        )

    def update_once(self):

        stats = rclone_api.get_stats()

        storage = rclone_api.get_storage()

        transfer = rclone_api.get_current_transfer()

        history_tracker.tick()

        self.status_card.update(
            stats,
            transfer
        )

        self.progress_card.update(
            stats,
            storage,
            transfer
        )

        if transfer:

            self.graph.add(
                transfer.get("speed", 0)
            )

        else:

            self.graph.add(0)

        self.graph_card.redraw()

        now = time.time()

        if now - self.last_activity_refresh >= 10:

            self.activity_card.refresh()

            self.last_activity_refresh = now

        if stats.get("connected"):

            self.app.title(
                f"Cloud Dashboard | "
                f"{len(stats.get('transferring', []))} Transfer(s)"
            )

        else:

            self.app.title(
                "Cloud Dashboard"
            )