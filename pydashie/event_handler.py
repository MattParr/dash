class EventHandler:
    def __init__(self):
        self.events_queue = {}
        self.last_events = {}
        self.using_events = True
        self.MAX_QUEUE_LENGTH = 20
