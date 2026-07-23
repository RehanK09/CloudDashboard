from api import rclone_api


class API:

    def __init__(self):

        self.rc = rclone_api

    def start(self):

        self.rc.start()

    def stop(self):

        self.rc.stop()

    def stats(self):

        return self.rc.get_stats()

    def storage(self):

        return self.rc.get_storage()

    def transfer(self):

        return self.rc.get_current_transfer()

    def pause(self):

        self.rc.pause_uploads()

    def resume(self):

        self.rc.resume_uploads()

    def stop_all(self):

        self.rc.stop_all()


api = API()