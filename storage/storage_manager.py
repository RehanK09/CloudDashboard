from core.config import config

from storage.drive import Drive


class StorageManager:

    def __init__(self):

        self.drives = []

        self.load()

    # =====================================================

    def load(self):

        self.drives.clear()

        for item in config.drives:

            self.drives.append(

                Drive(

                    name=item.get(
                        "name",
                        "Unknown Drive"
                    ),

                    remote=item.get(
                        "remote",
                        ""
                    ),

                    letter=item.get(
                        "drive",
                        "?"
                    )

                )

            )

    # =====================================================

    def reload(self):

        config.reload()

        self.load()

    # =====================================================

    def get(self):

        return self.drives

    # =====================================================

    def get_drive(

        self,

        letter

    ):

        for drive in self.drives:

            if drive.letter.upper() == letter.upper():

                return drive

        return None

    # =====================================================

    def update_storage(

        self,

        letter,

        used,

        free,

        total

    ):

        drive = self.get_drive(letter)

        if drive is None:

            return

        drive.connected = True

        drive.update_storage(

            used,

            free,

            total

        )

    # =====================================================

    def update_activity(

        self,

        letter,

        **kwargs

    ):

        drive = self.get_drive(letter)

        if drive is None:

            return

        drive.connected = True

        drive.update_activity(

            **kwargs

        )

    # =====================================================

    def disconnect(

        self,

        letter

    ):

        drive = self.get_drive(letter)

        if drive:

            drive.connected = False

            drive.speed_up = 0

            drive.speed_down = 0

            drive.transfers = 0

    # =====================================================

    def disconnect_all(self):

        for drive in self.drives:

            drive.connected = False

            drive.speed_up = 0

            drive.speed_down = 0

            drive.transfers = 0