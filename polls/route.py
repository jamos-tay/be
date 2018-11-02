
class Route():
    handler = None
    requires_auth = True

    def __init__(self, handler, requires_auth=True):
        self.handler = handler
        self.requires_auth = requires_auth
