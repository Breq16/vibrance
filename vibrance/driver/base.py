class BaseDriver:
    def __init__(self, name=""):
        self.name = name
        self.enabled = False

    def _open(self):
        pass

    def _close(self):
        pass

    def _read(self):
        return tuple()

    def open(self):
        if not self.enabled:
            self._open()
        self.enabled = True

    def close(self):
        if self.enabled:
            self._close()
        self.enabled = False

    def read(self):
        if self.enabled:
            return self._read()
        else:
            return tuple()

    def getStatus(self):
        status = {}
        status["health"] = "inactive"
        status["message"] = "No Driver"

        return status
