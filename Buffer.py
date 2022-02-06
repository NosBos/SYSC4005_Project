from Framework import Entity, Event, Simulation
from Component import Component
from WorkStation import WorkStation
from Inspector import Inspector


class Buffer (Entity):

    def start(self) -> None:
        pass

    def handle_event(self, event: Event) -> None:
        pass

    def end(self, clock) -> None:
        pass

    def __init__(self, simulation: Simulation, component_type: Component, priority: int):
        self.sim = simulation
        self.componentType = component_type
        self.priority = priority
        self.queue = []
        self.work_station = None
        self.inspector = None

    def add_work_station(self, work_station: WorkStation) -> None:
        self.work_station = work_station

    def add_inspector(self, inspector: Inspector) -> None:
        self.inspector = inspector

    def add_component(self, component: Component) -> None:
        self.queue.append(component)

    def pop_component(self) -> Component:
        return self.queue.pop(0)


