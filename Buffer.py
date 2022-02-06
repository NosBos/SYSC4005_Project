from Component import Component
from WorkStation import WorkStation
from Inspector import Inspector


class Buffer:

    def __init__(self, component_type: Component, priority: int):
        self.componentType = component_type
        self.priority = priority
        self.queue = []
        self.work_station = None
        self.inspector = None

    def add_work_station(self, work_station: WorkStation):
        self.work_station = work_station

    def add_inspector(self, inspector: Inspector):
        self.inspector = inspector

    def add_component(self, component: Component):
        self.queue.append(component)

    def pop_component(self):
        return self.queue.pop(0)


