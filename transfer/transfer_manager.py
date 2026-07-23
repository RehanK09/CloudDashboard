from core.api import api

from transfer.upload_queue import UploadQueue
from transfer.download_queue import DownloadQueue


class TransferManager:

    def __init__(

        self,

        parent

    ):

        self.uploads = UploadQueue(

            parent

        )

        self.downloads = DownloadQueue(

            parent

        )

    # ---------------------------------------------------------

    def pack(self):

        self.uploads.pack(

            fill="both",

            expand=True,

            padx=10,

            pady=(10,5)

        )

        self.downloads.pack(

            fill="both",

            expand=True,

            padx=10,

            pady=(5,10)

        )

    # ---------------------------------------------------------

    def refresh(self):

        stats = api.stats()

        self.uploads.update(

            stats

        )

        self.downloads.update(

            stats

        )

    # ---------------------------------------------------------

    def start(self, app):

        self.refresh()

        app.after(

            100,

            lambda: self.start(app)

        )