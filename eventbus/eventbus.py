from eventbus.event import Event

class EventBus:

    __event_bus_loaded = False

    __queue_map = {}

    def __init__(self):
        self.register_event(Event.ON_START)
        self.register_event(Event.ON_STOP)

    def register(self, event: Event, function):
        self.__queue_map[event].append(function)

    def register_queue(self, event: Event, queue: list):
        for callable in queue:
            self.__queue_map[event].append(callable)

    def register_event(self, event: Event):
        self.__queue_map[event] = []

    def fire_event(self, event: Event):
        for callable in self.__queue_map[event]:
            callable()

    def start(self):
        if self.__event_bus_loaded == False:
            for callable in self.__queue_map[Event.ON_START]:
                callable()
        self.__event_bus_loaded = True

    def stop(self):
        if self.__event_bus_loaded == True:
            for callable in self.__queue_map[Event.ON_STOP]:
                callable()
        self.__event_bus_loaded = False
    