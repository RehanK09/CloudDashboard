from dataclasses import dataclass


@dataclass
class Drive:

    name: str

    remote: str

    letter: str

    total: int = 0

    used: int = 0

    free: int = 0

    connected: bool = False

    uploading: bool = False

    downloading: bool = False

    speed_up: int = 0

    speed_down: int = 0

    transfers: int = 0

    errors: int = 0

    def update_storage(

        self,

        used,

        free,

        total

    ):

        self.used = int(used)

        self.free = int(free)

        self.total = int(total)

    def update_activity(

        self,

        uploading=False,

        downloading=False,

        speed_up=0,

        speed_down=0,

        transfers=0,

        errors=0

    ):

        self.uploading = uploading

        self.downloading = downloading

        self.speed_up = int(speed_up)

        self.speed_down = int(speed_down)

        self.transfers = transfers

        self.errors = errors

    @property
    def percent(self):

        if self.total <= 0:

            return 0

        return (self.used / self.total) * 100

    @property
    def status(self):

        if not self.connected:

            return "Offline"

        if self.errors:

            return "Error"

        if self.uploading and self.downloading:

            return "Syncing"

        if self.uploading:

            return "Uploading"

        if self.downloading:

            return "Downloading"

        return "Idle"

    @property
    def color(self):

        if not self.connected:

            return "#E53935"

        if self.errors:

            return "#D32F2F"

        if self.uploading:

            return "#2196F3"

        if self.downloading:

            return "#43A047"

        return "#9E9E9E"