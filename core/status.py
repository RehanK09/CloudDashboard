from enum import Enum


class AppState(Enum):

    OFFLINE = "OFFLINE"

    IDLE = "IDLE"

    UPLOADING = "UPLOADING"

    DOWNLOADING = "DOWNLOADING"

    SYNCING = "SYNCING"

    PAUSED = "PAUSED"

    ERROR = "ERROR"


class StatusEngine:

    def __init__(self):

        self.state = AppState.OFFLINE

        self.connected = False

        self.uploading = False

        self.downloading = False

        self.paused = False

        self.errors = 0

        self.upload_count = 0

        self.download_count = 0

    def update(

        self,

        connected=False,

        uploading=False,

        downloading=False,

        paused=False,

        errors=0,

        upload_count=0,

        download_count=0

    ):

        self.connected = connected

        self.uploading = uploading

        self.downloading = downloading

        self.paused = paused

        self.errors = errors

        self.upload_count = upload_count

        self.download_count = download_count

        self._compute()

    def _compute(self):

        if not self.connected:

            self.state = AppState.OFFLINE

            return

        if self.errors > 0:

            self.state = AppState.ERROR

            return

        if self.paused:

            self.state = AppState.PAUSED

            return

        if self.uploading and self.downloading:

            self.state = AppState.SYNCING

            return

        if self.uploading:

            self.state = AppState.UPLOADING

            return

        if self.downloading:

            self.state = AppState.DOWNLOADING

            return

        self.state = AppState.IDLE

    @property
    def text(self):

        return self.state.value

    @property
    def color(self):

        colors = {

            AppState.OFFLINE: "#C62828",

            AppState.ERROR: "#E53935",

            AppState.PAUSED: "#F9A825",

            AppState.UPLOADING: "#1976D2",

            AppState.DOWNLOADING: "#2E7D32",

            AppState.SYNCING: "#7B1FA2",

            AppState.IDLE: "#616161"

        }

        return colors[self.state]

    @property
    def title(self):

        titles = {

            AppState.OFFLINE: "Offline",

            AppState.ERROR: "Error",

            AppState.PAUSED: "Paused",

            AppState.UPLOADING: f"Uploading ({self.upload_count})",

            AppState.DOWNLOADING: f"Downloading ({self.download_count})",

            AppState.SYNCING: f"Syncing ({self.upload_count + self.download_count})",

            AppState.IDLE: "Idle"

        }

        return titles[self.state]


status = StatusEngine()