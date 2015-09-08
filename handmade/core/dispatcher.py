from kivy.event import EventDispatcher


class CoreEventsDispatcher(EventDispatcher):
    def on_initialization(self):
        pass

    def __init__(self):
        super(CoreEventsDispatcher, self).__init__()
        self.register_event_type('on_initialization')


events = CoreEventsDispatcher()
