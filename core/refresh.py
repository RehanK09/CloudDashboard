import threading
import time

from core.api import api
from core.status import status


class RefreshManager:

    def __init__(self, dashboard):

        self.dashboard = dashboard

        self.api = api

        self.running = False

        self.thread = None

    # =====================================================

    def start(self):

        if self.running:

            return

        self.running = True

        self.api.start()

        self.thread = threading.Thread(

            target=self.loop,

            daemon=True

        )

        self.thread.start()

    # =====================================================

    def stop(self):

        self.running = False

    # =====================================================

    def loop(self):

        while self.running:

            try:

                stats = self.api.stats()

                storage = self.api.storage()

                transfer = self.api.transfer()

                connected = stats.get(

                    "connected",

                    False

                )

                transferring = stats.get(

                    "transferring",

                    []

                )

                uploading = len(

                    transferring

                ) > 0

                #
                # Download detection will be added later
                #

                downloading = False

                paused = False

                errors = stats.get(

                    "errors",

                    0

                )

                status.update(

                    connected=connected,

                    uploading=uploading,

                    downloading=downloading,

                    paused=paused,

                    errors=errors,

                    upload_count=len(

                        transferring

                    ),

                    download_count=0

                )

                self.dashboard.app.after(

                    0,

                    lambda s=stats, st=storage, t=transfer:

                    self.update_ui(

                        s,

                        st,

                        t

                    )

                )

            except Exception as e:

                print(

                    "Refresh:",

                    e

                )

            #
            # Adaptive refresh
            #

            if uploading:

                time.sleep(

                    0.10

                )

            else:

                time.sleep(

                    0.50

                )

    # =====================================================

    def update_ui(

        self,

        stats,

        storage,

        transfer

    ):

        try:

            self.dashboard.header.refresh(

                stats

            )

        except:

            pass

        try:

            self.dashboard.storage.refresh(

                storage,

                stats

            )

        except:

            pass

        try:

            self.dashboard.transfer_manager.refresh()

        except:

            pass

        try:

            self.dashboard.graph.update(

                stats

            )

        except:

            pass

        try:

            self.dashboard.stats.update(

                stats,

                storage

            )

        except:

            pass

        try:
        
            self.dashboard.upload_panel.refresh(
            
                stats.get(
                
                    "transferring",
        
                    []
        
                )
        
            )
        
        except:
        
            pass