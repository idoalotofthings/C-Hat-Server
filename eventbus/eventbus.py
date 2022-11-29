from event import Event

class EventBus:

    __event_bus_loaded = False

    __queue_map = {}

    __on_start_queue = []
    __on_stop_queue = []

    def register(self, event: Event, function):
        self.__queue_map[event].append(function)

    def register_queue(self, event: Event, queue: list):
        for callable in queue:
            self.__queue_map[event].append(callable)

    def register_event(self, event: Event):
        self.__queue_map[event].append([])

    def start(self):
        if self.__event_bus_loaded == False:
            for callable in self.__on_start_queue:
                callable()
        self.__event_bus_loaded = True

    def stop(self):
        if self.__event_bus_loaded == True:
            for callable in self.__on_stop_queue:
                callable()
        self.__event_bus_loaded = False
    