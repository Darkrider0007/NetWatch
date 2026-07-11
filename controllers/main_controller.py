class MainController:

    def __init__(self):

        self.monitor = None

    def start(self):

        if self.monitor:

            self.monitor.start()

    def stop(self):

        if self.monitor:

            self.monitor.stop()