import json
import os


class Config:

    def __init__(self, path="config.json"):

        self.path = path

        self.reload()

    def reload(self):

        if not os.path.exists(self.path):

            self.data = {

                "rc_port": 5572,

                "history_limit": 500,

                "theme": "dark",

                "drives": []

            }

            return

        with open(self.path, "r", encoding="utf-8") as f:

            self.data = json.load(f)

    def save(self):

        with open(self.path, "w", encoding="utf-8") as f:

            json.dump(

                self.data,

                f,

                indent=4

            )

    @property
    def rc_port(self):

        return self.data.get(
            "rc_port",
            5572
        )

    @property
    def history_limit(self):

        return self.data.get(
            "history_limit",
            500
        )

    @property
    def theme(self):

        return self.data.get(
            "theme",
            "dark"
        )

    @property
    def drives(self):

        return self.data.get(
            "drives",
            []
        )

    def get_drive(self, index=0):

        if index >= len(self.drives):

            return None

        return self.drives[index]

    def add_drive(

        self,

        name,

        remote,

        drive,

        rclone

    ):

        self.data.setdefault(
            "drives",
            []
        ).append(

            {

                "name": name,

                "remote": remote,

                "drive": drive,

                "rclone": rclone

            }

        )

        self.save()

    def remove_drive(self, index):

        if index < len(self.drives):

            self.data["drives"].pop(index)

            self.save()

    def update_drive(

        self,

        index,

        **kwargs

    ):

        if index >= len(self.drives):

            return

        self.data["drives"][index].update(kwargs)

        self.save()


config = Config()