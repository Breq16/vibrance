class BaseDriver:
    def __init__(self, name=""):
        self.name = name
        self.enabled = False

    def open(self):
        self.enabled = True

    def close(self):
        self.enabled = False

    def read(self):
        return tuple()

    def getStatus(self):
        status = {}
        status["health"] = "inactive"
        status["message"] = "No Driver"

        return status
