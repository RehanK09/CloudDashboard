from dataclasses import dataclass


@dataclass
class Transfer:

    name: str

    direction: str = "upload"

    size: int = 0

    transferred: int = 0

    speed: int = 0

    eta: int | None = None

    progress: float = 0.0

    status: str = "waiting"

    started: float = 0

    finished: float = 0

    error: str = ""

    @property
    def active(self):

        return self.status in (

            "uploading",

            "downloading"

        )

    @property
    def completed(self):

        return self.status == "completed"

    @property
    def failed(self):

        return self.status == "failed"

    @property
    def paused(self):

        return self.status == "paused"

    def update(

        self,

        **kwargs

    ):

        for key, value in kwargs.items():

            if hasattr(self, key):

                setattr(

                    self,

                    key,

                    value

                )

        if self.size > 0:

            self.progress = (

                self.transferred

                /

                self.size

            ) * 100

        else:

            self.progress = 0

    def reset(self):

        self.transferred = 0

        self.speed = 0

        self.progress = 0

        self.eta = None

        self.status = "waiting"

        self.error = ""